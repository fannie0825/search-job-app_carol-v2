"""Resume embedding generation and storage"""
import streamlit as st
from modules.utils import get_embedding_generator, get_token_tracker


def generate_and_store_resume_embedding(resume_text, user_profile=None):
    """Generate embedding for resume and store in session state.
    
    This is called once when resume is uploaded/updated, so we can reuse
    the embedding for all subsequent searches without regenerating it.
    """
    if not resume_text:
        st.session_state.resume_embedding = None
        return None
    
    # Build resume query text
    if user_profile:
        profile_data = f"{user_profile.get('summary', '')} {user_profile.get('experience', '')} {user_profile.get('skills', '')}"
        resume_query = f"{resume_text} {profile_data}"
    else:
        resume_query = resume_text
    
    # Generate embedding
    embedding_gen = get_embedding_generator()
    if not embedding_gen:
        return None
    
    embedding, tokens_used = embedding_gen.get_embedding(resume_query)
    
    # Update token tracker
    token_tracker = get_token_tracker()
    if token_tracker:
        token_tracker.add_embedding_tokens(tokens_used)
    
    if embedding:
        st.session_state.resume_embedding = embedding
        return embedding
    
    return None
