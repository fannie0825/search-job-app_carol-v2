"""Semantic job search functionality"""
import os
import hashlib
import streamlit as st
import numpy as np
import chromadb
from sklearn.metrics.pairwise import cosine_similarity
from modules.utils import get_token_tracker, _is_streamlit_cloud
from modules.utils.config import DEFAULT_MAX_JOBS_TO_INDEX, USE_FAST_SKILL_MATCHING


class SemanticJobSearch:
    """Semantic job search using embeddings"""
    def __init__(self, embedding_generator, use_persistent_store=True):
        self.embedding_gen = embedding_generator
        self.job_embeddings = []
        self.jobs = []
        self.chroma_client = None
        self.collection = None
        
        if _is_streamlit_cloud():
            use_persistent_store = False
        
        self.use_persistent_store = use_persistent_store
        
        if use_persistent_store:
            try:
                chroma_db_path = os.path.join(os.getcwd(), ".chroma_db")
                os.makedirs(chroma_db_path, exist_ok=True)
                self.chroma_client = chromadb.PersistentClient(path=chroma_db_path)
                self.collection = self.chroma_client.get_or_create_collection(
                    name="job_embeddings",
                    metadata={"hnsw:space": "cosine"}
                )
            except Exception as e:
                st.warning(f"⚠️ Could not initialize persistent vector store: {e}. Using in-memory storage.")
                self.use_persistent_store = False
        
        if not self.use_persistent_store and self.chroma_client is None:
            try:
                self.chroma_client = chromadb.EphemeralClient()
                self.collection = self.chroma_client.get_or_create_collection(
                    name="job_embeddings",
                    metadata={"hnsw:space": "cosine"}
                )
            except Exception as e:
                pass
    
    def _get_job_hash(self, job):
        """Generate a hash for a job to use as ID."""
        job_str = f"{job.get('title', '')}_{job.get('company', '')}_{job.get('url', '')}"
        return hashlib.md5(job_str.encode()).hexdigest()
    
    def index_jobs(self, jobs, max_jobs_to_index=None):
        """Simplified job indexing: Check if job exists, if not, embed and store."""
        if not jobs:
            st.warning("⚠️ No jobs available to index.")
            self.jobs = []
            self.job_embeddings = []
            return
        
        effective_limit = max_jobs_to_index or min(len(jobs), DEFAULT_MAX_JOBS_TO_INDEX)
        effective_limit = max(1, min(effective_limit, len(jobs)))
        if effective_limit < len(jobs):
            st.info(f"⚙️ Indexing first {effective_limit} of {len(jobs)} jobs to reduce embedding API calls.")
        jobs_to_index = jobs[:effective_limit]
        self.jobs = jobs_to_index
        job_texts = [
            f"{job['title']} at {job['company']}. {job['description']} Skills: {', '.join(job['skills'][:5])}"
            for job in jobs_to_index
        ]
        
        st.info(f"📊 Indexing {len(jobs_to_index)} jobs...")
        
        if self.use_persistent_store and self.collection:
            try:
                job_hashes = [self._get_job_hash(job) for job in jobs_to_index]
                existing_data = self.collection.get(ids=job_hashes, include=['embeddings'])
                existing_ids = set(existing_data.get('ids', [])) if existing_data else set()
                
                jobs_to_embed = []
                indices_to_embed = []
                for idx, job_hash in enumerate(job_hashes):
                    if job_hash not in existing_ids:
                        jobs_to_embed.append(job_texts[idx])
                        indices_to_embed.append(idx)
                
                if jobs_to_embed:
                    st.info(f"🔄 Generating embeddings for {len(jobs_to_embed)} new jobs...")
                    new_embeddings, tokens_used = self.embedding_gen.get_embeddings_batch(jobs_to_embed)
                    
                    token_tracker = get_token_tracker()
                    if token_tracker:
                        token_tracker.add_embedding_tokens(tokens_used)
                    
                    for idx, emb in zip(indices_to_embed, new_embeddings):
                        if emb:
                            job_hash = job_hashes[idx]
                            self.collection.upsert(
                                ids=[job_hash],
                                embeddings=[emb],
                                documents=[job_texts[idx]],
                                metadatas=[{"job_index": idx}]
                            )
                
                retrieved = self.collection.get(ids=job_hashes, include=['embeddings'])
                if retrieved and 'embeddings' in retrieved and retrieved['embeddings'] is not None and len(retrieved['embeddings']) > 0:
                    hash_to_emb = {h: e for h, e in zip(retrieved['ids'], retrieved['embeddings'])}
                    self.job_embeddings = [hash_to_emb.get(h, None) for h in job_hashes]
                    self.job_embeddings = [e for e in self.job_embeddings if e is not None]
                    st.success(f"✅ Indexed {len(self.job_embeddings)} jobs (using persistent store)")
                else:
                    self.job_embeddings, tokens_used = self.embedding_gen.get_embeddings_batch(job_texts)
                    token_tracker = get_token_tracker()
                    if token_tracker:
                        token_tracker.add_embedding_tokens(tokens_used)
                    st.success(f"✅ Indexed {len(self.job_embeddings)} jobs")
            except Exception as e:
                st.warning(f"⚠️ Error using persistent store: {e}. Generating new embeddings...")
                self.job_embeddings, tokens_used = self.embedding_gen.get_embeddings_batch(job_texts)
                token_tracker = get_token_tracker()
                if token_tracker:
                    token_tracker.add_embedding_tokens(tokens_used)
                self.use_persistent_store = False
                st.success(f"✅ Indexed {len(self.job_embeddings)} jobs")
        else:
            self.job_embeddings, tokens_used = self.embedding_gen.get_embeddings_batch(job_texts)
            token_tracker = get_token_tracker()
            if token_tracker:
                token_tracker.add_embedding_tokens(tokens_used)
            st.success(f"✅ Indexed {len(self.job_embeddings)} jobs")
    
    def search(self, query=None, top_k=10, resume_embedding=None):
        """Simplified search: Use pre-computed resume embedding if available, otherwise generate from query."""
        if not self.job_embeddings:
            return []
        
        if resume_embedding is not None:
            query_embedding = resume_embedding
        elif query:
            query_embedding, tokens_used = self.embedding_gen.get_embedding(query)
            token_tracker = get_token_tracker()
            if token_tracker:
                token_tracker.add_embedding_tokens(tokens_used)
            if not query_embedding:
                return []
        else:
            return []
        
        query_emb = np.array(query_embedding).reshape(1, -1)
        job_embs = np.array(self.job_embeddings)
        
        similarities = cosine_similarity(query_emb, job_embs)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                'job': self.jobs[idx],
                'similarity_score': float(similarities[idx]),
                'rank': len(results) + 1
            })
        
        return results
    
    def calculate_skill_match(self, user_skills, job_skills):
        """Calculate skill-based match score."""
        if not user_skills or not job_skills:
            return 0.0, []
        
        user_skills_list = [s.strip() for s in str(user_skills).split(',') if s.strip()]
        job_skills_list = [s.strip() for s in job_skills if isinstance(s, str) and s.strip()]
        
        if not user_skills_list or not job_skills_list:
            return 0.0, []
        
        if USE_FAST_SKILL_MATCHING:
            return self._calculate_skill_match_string_based(user_skills_list, job_skills_list)
        
        try:
            user_skills_key = ",".join(sorted(user_skills_list))
            if user_skills_key in st.session_state.user_skills_embeddings_cache:
                user_skill_embeddings = st.session_state.user_skills_embeddings_cache[user_skills_key]
                user_tokens = 0
            else:
                user_skill_embeddings, user_tokens = self.embedding_gen.get_embeddings_batch(user_skills_list, batch_size=10)
                if user_skill_embeddings:
                    st.session_state.user_skills_embeddings_cache[user_skills_key] = user_skill_embeddings
            
            job_skills_key = ",".join(sorted(job_skills_list))
            if job_skills_key in st.session_state.skill_embeddings_cache:
                job_skill_embeddings = st.session_state.skill_embeddings_cache[job_skills_key]
                job_tokens = 0
            else:
                job_skill_embeddings, job_tokens = self.embedding_gen.get_embeddings_batch(job_skills_list, batch_size=10)
                if job_skill_embeddings:
                    st.session_state.skill_embeddings_cache[job_skills_key] = job_skill_embeddings
            
            if user_tokens > 0 or job_tokens > 0:
                token_tracker = get_token_tracker()
                if token_tracker:
                    token_tracker.add_embedding_tokens(user_tokens + job_tokens)
            
            if not user_skill_embeddings or not job_skill_embeddings:
                return self._calculate_skill_match_string_based(user_skills_list, job_skills_list)
            
            user_embs = np.array(user_skill_embeddings)
            job_embs = np.array(job_skill_embeddings)
            
            similarity_matrix = cosine_similarity(job_embs, user_embs)
            
            similarity_threshold = 0.7
            matched_skills = []
            matched_indices = set()
            
            for job_idx, job_skill in enumerate(job_skills_list):
                best_match_idx = np.argmax(similarity_matrix[job_idx])
                best_similarity = similarity_matrix[job_idx][best_match_idx]
                
                if best_similarity >= similarity_threshold and best_match_idx not in matched_indices:
                    matched_skills.append(job_skill)
                    matched_indices.add(best_match_idx)
            
            match_score = len(matched_skills) / len(job_skills_list) if job_skills_list else 0.0
            missing_skills = [js for js in job_skills_list if js not in matched_skills]
            
            return min(match_score, 1.0), missing_skills[:5]
            
        except Exception as e:
            return self._calculate_skill_match_string_based(user_skills_list, job_skills_list)
    
    def _calculate_skill_match_string_based(self, user_skills_list, job_skills_list):
        """Fallback string-based skill matching"""
        user_skills_lower = [s.lower() for s in user_skills_list]
        job_skills_lower = [s.lower() for s in job_skills_list]
        
        matched_skills = []
        for job_skill in job_skills_lower:
            for user_skill in user_skills_lower:
                if job_skill in user_skill or user_skill in job_skill:
                    matched_skills.append(job_skill)
                    break
        
        match_score = len(matched_skills) / len(job_skills_lower) if job_skills_lower else 0.0
        missing_skills = [job_skills_list[i] for i, js in enumerate(job_skills_lower) if js not in matched_skills]
        
        return min(match_score, 1.0), missing_skills[:5]
