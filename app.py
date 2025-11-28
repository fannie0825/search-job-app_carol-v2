import warnings
import os
warnings.filterwarnings('ignore')
os.environ['STREAMLIT_LOG_LEVEL'] = 'error'

import streamlit as st
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import time
from datetime import datetime
import json
import re
from io import BytesIO
import PyPDF2
from docx import Document

st.set_page_config(
    page_title="Semantic Job Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(120deg, #1f77b4, #2ecc71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .job-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .job-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .match-score {
        background: linear-gradient(120deg, #1f77b4, #2ecc71);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        font-size: 0.9rem;
    }
    .tag {
        display: inline-block;
        background-color: #e9ecef;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        margin: 0.2rem;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'jobs_cache' not in st.session_state:
    st.session_state.jobs_cache = {}
if 'embedding_gen' not in st.session_state:
    st.session_state.embedding_gen = None
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'generated_resume' not in st.session_state:
    st.session_state.generated_resume = None
if 'text_gen' not in st.session_state:
    st.session_state.text_gen = None
if 'selected_job' not in st.session_state:
    st.session_state.selected_job = None
if 'show_resume_generator' not in st.session_state:
    st.session_state.show_resume_generator = False
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
if 'matched_jobs' not in st.session_state:
    st.session_state.matched_jobs = []

class APIMEmbeddingGenerator:
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        # Normalize endpoint: remove trailing slash
        endpoint = endpoint.rstrip('/')
        # Remove /openai if it's already in the endpoint (to avoid duplication)
        if endpoint.endswith('/openai'):
            endpoint = endpoint[:-7]  # Remove '/openai'
        self.endpoint = endpoint
        self.deployment = "text-embedding-3-small"
        self.api_version = "2024-02-01"
        self.url = f"{self.endpoint}/openai/deployments/{self.deployment}/embeddings?api-version={self.api_version}"
        self.headers = {"api-key": self.api_key, "Content-Type": "application/json"}
    
    def get_embedding(self, text):
        try:
            payload = {"input": text, "model": self.deployment}
            response = requests.post(self.url, headers=self.headers, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()['data'][0]['embedding']
            return None
        except Exception as e:
            st.error(f"Error: {e}")
            return None
    
    def get_embeddings_batch(self, texts, batch_size=10):
        embeddings = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            progress = (i + len(batch)) / len(texts)
            progress_bar.progress(progress)
            status_text.text(f"🔄 Generating embeddings: {i + len(batch)}/{len(texts)}")
            
            try:
                payload = {"input": batch, "model": self.deployment}
                response = requests.post(self.url, headers=self.headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    sorted_data = sorted(data['data'], key=lambda x: x['index'])
                    embeddings.extend([item['embedding'] for item in sorted_data])
            except:
                for text in batch:
                    emb = self.get_embedding(text)
                    if emb:
                        embeddings.append(emb)
        
        progress_bar.empty()
        status_text.empty()
        return embeddings

class AzureOpenAITextGenerator:
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        # Normalize endpoint: remove trailing slash
        endpoint = endpoint.rstrip('/')
        # Remove /openai if it's already in the endpoint (to avoid duplication)
        if endpoint.endswith('/openai'):
            endpoint = endpoint[:-7]  # Remove '/openai'
        self.endpoint = endpoint
        self.deployment = "gpt-4o-mini"  # or your deployment name
        self.api_version = "2024-02-01"
        self.url = f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version={self.api_version}"
        self.headers = {"api-key": self.api_key, "Content-Type": "application/json"}
    
    def generate_resume(self, user_profile, job_posting):
        """Generate a tailored resume based on user profile and job posting"""
        prompt = f"""You are an expert resume writer. Create a professional, ATS-friendly resume tailored to the specific job posting.

USER BACKGROUND:
- Name: {user_profile.get('name', 'N/A')}
- Email: {user_profile.get('email', 'N/A')}
- Phone: {user_profile.get('phone', 'N/A')}
- Location: {user_profile.get('location', 'N/A')}
- Summary: {user_profile.get('summary', 'N/A')}
- Experience: {user_profile.get('experience', 'N/A')}
- Education: {user_profile.get('education', 'N/A')}
- Skills: {user_profile.get('skills', 'N/A')}
- Certifications: {user_profile.get('certifications', 'N/A')}

JOB POSTING:
- Title: {job_posting.get('title', 'N/A')}
- Company: {job_posting.get('company', 'N/A')}
- Description: {job_posting.get('description', 'N/A')}
- Required Skills: {', '.join(job_posting.get('skills', []))}

Please create a tailored resume that:
1. Highlights relevant experience matching the job requirements
2. Emphasizes skills mentioned in the job posting
3. Uses keywords from the job description for ATS optimization
4. Maintains a professional and concise format
5. Focuses on achievements and measurable results

Format the resume in a clean, professional text format with clear sections."""
        
        try:
            payload = {
                "messages": [
                    {"role": "system", "content": "You are a professional resume writer with expertise in ATS optimization and career coaching."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2000,
                "temperature": 0.7
            }
            
            response = requests.post(self.url, headers=self.headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            st.error(f"Error generating resume: {e}")
            return None

class IndeedScraperAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://indeed-scraper-api.p.rapidapi.com/api/job"
        self.headers = {
            'Content-Type': 'application/json',
            'x-rapidapi-host': 'indeed-scraper-api.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
    
    def search_jobs(self, query, location="Hong Kong", max_rows=15, job_type="fulltime", country="hk"):
        payload = {
            "scraper": {
                "maxRows": max_rows,
                "query": query,
                "location": location,
                "jobType": job_type,
                "radius": "50",
                "sort": "relevance",
                "fromDays": "7",
                "country": country
            }
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=payload, timeout=60)
            
            if response.status_code == 201:
                data = response.json()
                jobs = []
                
                if 'returnvalue' in data and 'data' in data['returnvalue']:
                    job_list = data['returnvalue']['data']
                    
                    for job_data in job_list:
                        parsed_job = self._parse_job(job_data)
                        if parsed_job:
                            jobs.append(parsed_job)
                
                return jobs
            else:
                st.error(f"API Error: {response.status_code}")
                return []
                
        except Exception as e:
            st.error(f"Error: {e}")
            return []
    
    def _parse_job(self, job_data):
        try:
            location_data = job_data.get('location', {})
            location = location_data.get('formattedAddressShort') or location_data.get('city', 'Hong Kong')
            
            job_types = job_data.get('jobType', [])
            job_type = ', '.join(job_types) if job_types else 'Full-time'
            
            benefits = job_data.get('benefits', [])
            attributes = job_data.get('attributes', [])
            
            return {
                'title': job_data.get('title', 'N/A'),
                'company': job_data.get('companyName', 'N/A'),
                'location': location,
                'description': job_data.get('descriptionText', 'No description')[:2000],
                'salary': 'Not specified',
                'job_type': job_type,
                'url': job_data.get('jobUrl', '#'),
                'posted_date': job_data.get('age', 'Recently'),
                'benefits': benefits[:5],
                'skills': attributes[:10],
                'company_rating': job_data.get('rating', {}).get('rating', 0),
                'is_remote': job_data.get('isRemote', False)
            }
        except:
            return None

class SemanticJobSearch:
    def __init__(self, embedding_generator):
        self.embedding_gen = embedding_generator
        self.job_embeddings = []
        self.jobs = []
    
    def index_jobs(self, jobs):
        self.jobs = jobs
        job_texts = [
            f"{job['title']} at {job['company']}. {job['description']} Skills: {', '.join(job['skills'][:5])}"
            for job in jobs
        ]
        
        st.info(f"📊 Indexing {len(jobs)} jobs...")
        self.job_embeddings = self.embedding_gen.get_embeddings_batch(job_texts)
        st.success(f"✅ Indexed {len(self.job_embeddings)} jobs")
    
    def search(self, query, top_k=10):
        if not self.job_embeddings:
            return []
        
        query_embedding = self.embedding_gen.get_embedding(query)
        if not query_embedding:
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

def get_embedding_generator():
    if st.session_state.embedding_gen is None:
        # Use secrets instead of hardcoded values
        AZURE_OPENAI_API_KEY = st.secrets["AZURE_OPENAI_API_KEY"]
        AZURE_OPENAI_ENDPOINT = st.secrets["AZURE_OPENAI_ENDPOINT"]
        st.session_state.embedding_gen = APIMEmbeddingGenerator(AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT)
    return st.session_state.embedding_gen

def get_job_scraper():
    # Use secrets instead of hardcoded values
    RAPIDAPI_KEY = st.secrets["RAPIDAPI_KEY"]
    return IndeedScraperAPI(RAPIDAPI_KEY)

def get_text_generator():
    if st.session_state.text_gen is None:
        AZURE_OPENAI_API_KEY = st.secrets["AZURE_OPENAI_API_KEY"]
        AZURE_OPENAI_ENDPOINT = st.secrets["AZURE_OPENAI_ENDPOINT"]
        st.session_state.text_gen = AzureOpenAITextGenerator(AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT)
    return st.session_state.text_gen

def display_job_card(result, index):
    job = result['job']
    score = result['similarity_score']
    
    remote_badge = "🏠 Remote" if job['is_remote'] else ""
    rating = job['company_rating']
    stars = "⭐" * int(rating) if rating > 0 else ""
    
    st.markdown(f"""
    <div class="job-card">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
            <div style="flex-grow: 1;">
                <h3 style="margin: 0; color: #1f77b4;">#{index} {job['title']}</h3>
                <p style="margin: 0.5rem 0; color: #666; font-size: 0.95rem;">
                    🏢 <strong>{job['company']}</strong> {stars} • 📍 {job['location']} {remote_badge}
                </p>
            </div>
            <div class="match-score">
                {score:.1%} Match
            </div>
        </div>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 0.5rem;">
            <span>⏰ {job['job_type']}</span>
            <span>💰 {job['salary']}</span>
            <span>📅 {job['posted_date']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if job['benefits']:
            st.write("**Benefits:**")
            for benefit in job['benefits']:
                st.markdown(f'<span class="tag">✓ {benefit}</span>', unsafe_allow_html=True)
    
    with col2:
        if job['skills']:
            st.write("**Skills:**")
            skills_text = " ".join([f'<span class="tag">{skill}</span>' for skill in job['skills'][:8]])
            st.markdown(skills_text, unsafe_allow_html=True)
    
    st.write("")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        with st.expander("📝 View Full Description"):
            st.write(job['description'])
    
    with col2:
        col2a, col2b = st.columns(2)
        with col2a:
            if job['url'] != '#':
                st.link_button("Apply →", job['url'], use_container_width=True)
        with col2b:
            if st.button("📄 Resume", key=f"resume_{index}", use_container_width=True, type="primary"):
                st.session_state.selected_job = job
                st.session_state.show_resume_generator = True
                st.rerun()

def extract_text_from_resume(uploaded_file):
    """Extract text from uploaded resume file (PDF, DOCX, or TXT)"""
    try:
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        if file_type == 'pdf':
            # Extract text from PDF
            uploaded_file.seek(0)  # Reset file pointer
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        
        elif file_type == 'docx':
            # Extract text from DOCX
            uploaded_file.seek(0)  # Reset file pointer
            doc = Document(uploaded_file)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        
        elif file_type == 'txt':
            # Read text file
            uploaded_file.seek(0)  # Reset file pointer
            text = str(uploaded_file.read(), "utf-8")
            return text
        
        else:
            st.error(f"Unsupported file type: {file_type}. Please upload PDF, DOCX, or TXT.")
            return None
            
    except Exception as e:
        st.error(f"Error extracting text from resume: {e}")
        return None

def extract_profile_from_resume(resume_text):
    """Use Azure OpenAI to extract structured profile information from resume text"""
    try:
        text_gen = get_text_generator()
        
        prompt = f"""You are an expert at parsing resumes. Extract structured information from the following resume text.

RESUME TEXT:
{resume_text}

Please extract and return the following information in JSON format:
{{
    "name": "Full name",
    "email": "Email address",
    "phone": "Phone number",
    "location": "City, State/Country",
    "linkedin": "LinkedIn URL if mentioned",
    "portfolio": "Portfolio/website URL if mentioned",
    "summary": "Professional summary or objective (2-3 sentences)",
    "experience": "Work experience in chronological order with job titles, companies, dates, and key achievements (formatted as bullet points)",
    "education": "Education details including degrees, institutions, and graduation dates",
    "skills": "Comma-separated list of technical and soft skills",
    "certifications": "Professional certifications, awards, publications, or other achievements"
}}

Important:
- If information is not found, use "N/A" or empty string
- Format experience with clear job titles, companies, dates, and bullet points for achievements
- Extract all relevant skills mentioned
- Keep the summary concise but informative
- Return ONLY valid JSON, no additional text or markdown"""
        
        payload = {
            "messages": [
                {"role": "system", "content": "You are a resume parser. Extract structured information and return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.3
        }
        
        response = requests.post(
            text_gen.url,
            headers=text_gen.headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Try to extract JSON from the response
            # Sometimes the model returns JSON wrapped in markdown code blocks
            content = content.strip()
            if content.startswith("```"):
                # Remove markdown code blocks
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1]) if lines[-1].startswith('```') else '\n'.join(lines[1:])
            
            try:
                profile_data = json.loads(content)
                return profile_data
            except json.JSONDecodeError:
                # Try to find JSON in the response
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    profile_data = json.loads(json_match.group())
                    return profile_data
                else:
                    st.error("Could not parse extracted profile data. Please try again.")
                    return None
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.error(f"Error extracting profile: {e}")
        return None

def display_user_profile():
    """Display and edit user profile"""
    st.header("👤 Your Profile")
    st.caption("Fill in your information to generate tailored resumes")
    
    # Resume upload section
    st.markdown("---")
    st.subheader("📄 Upload Your Resume (Optional)")
    st.caption("Upload your resume to automatically extract your information")
    
    uploaded_file = st.file_uploader(
        "Choose a resume file",
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, DOCX, TXT"
    )
    
    if uploaded_file is not None:
        if st.button("🔍 Extract Information from Resume", type="primary", use_container_width=True):
            with st.spinner("📖 Reading resume and extracting information..."):
                # Extract text from resume
                resume_text = extract_text_from_resume(uploaded_file)
                
                if resume_text:
                    # Store resume text for job matching
                    st.session_state.resume_text = resume_text
                    st.success(f"✅ Extracted {len(resume_text)} characters from resume")
                    
                    # Show extracted text preview
                    with st.expander("📝 Preview Extracted Text"):
                        st.text(resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text)
                    
                    # Extract structured information
                    with st.spinner("🤖 Using AI to extract structured information..."):
                        profile_data = extract_profile_from_resume(resume_text)
                        
                        if profile_data:
                            # Update session state with extracted data
                            st.session_state.user_profile = {
                                'name': profile_data.get('name', ''),
                                'email': profile_data.get('email', ''),
                                'phone': profile_data.get('phone', ''),
                                'location': profile_data.get('location', ''),
                                'linkedin': profile_data.get('linkedin', ''),
                                'portfolio': profile_data.get('portfolio', ''),
                                'summary': profile_data.get('summary', ''),
                                'experience': profile_data.get('experience', ''),
                                'education': profile_data.get('education', ''),
                                'skills': profile_data.get('skills', ''),
                                'certifications': profile_data.get('certifications', '')
                            }
                            st.success("✅ Profile information extracted successfully! Review and edit below.")
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.warning("⚠️ Could not extract structured information. Please fill in manually.")
    
    st.markdown("---")
    
    with st.form("user_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", value=st.session_state.user_profile.get('name', ''))
            email = st.text_input("Email", value=st.session_state.user_profile.get('email', ''))
            phone = st.text_input("Phone", value=st.session_state.user_profile.get('phone', ''))
        
        with col2:
            location = st.text_input("Location", value=st.session_state.user_profile.get('location', ''))
            linkedin = st.text_input("LinkedIn URL", value=st.session_state.user_profile.get('linkedin', ''))
            portfolio = st.text_input("Portfolio/Website", value=st.session_state.user_profile.get('portfolio', ''))
        
        summary = st.text_area(
            "Professional Summary",
            value=st.session_state.user_profile.get('summary', ''),
            height=100,
            placeholder="Brief overview of your professional background..."
        )
        
        experience = st.text_area(
            "Work Experience",
            value=st.session_state.user_profile.get('experience', ''),
            height=150,
            placeholder="List your work experience with job titles, companies, dates, and key achievements..."
        )
        
        education = st.text_area(
            "Education",
            value=st.session_state.user_profile.get('education', ''),
            height=100,
            placeholder="Degrees, institutions, graduation dates..."
        )
        
        skills = st.text_area(
            "Skills",
            value=st.session_state.user_profile.get('skills', ''),
            height=80,
            placeholder="List your technical and soft skills (comma-separated)..."
        )
        
        certifications = st.text_area(
            "Certifications & Awards",
            value=st.session_state.user_profile.get('certifications', ''),
            height=80,
            placeholder="Professional certifications, awards, publications..."
        )
        
        submitted = st.form_submit_button("💾 Save Profile", use_container_width=True, type="primary")
        
        if submitted:
            st.session_state.user_profile = {
                'name': name,
                'email': email,
                'phone': phone,
                'location': location,
                'linkedin': linkedin,
                'portfolio': portfolio,
                'summary': summary,
                'experience': experience,
                'education': education,
                'skills': skills,
                'certifications': certifications
            }
            st.success("✅ Profile saved successfully!")
            time.sleep(1)
            st.rerun()

def display_resume_generator():
    """Display the resume generator interface"""
    if st.session_state.selected_job is None:
        st.warning("No job selected. Please select a job first.")
        if st.button("← Back to Jobs"):
            st.session_state.show_resume_generator = False
            st.rerun()
        return
    
    job = st.session_state.selected_job
    
    st.markdown('<h1 class="main-header">📄 Resume Generator</h1>', unsafe_allow_html=True)
    
    # Display selected job info
    st.markdown(f"""
    <div class="job-card">
        <h3 style="color: #1f77b4; margin: 0;">{job['title']}</h3>
        <p style="margin: 0.5rem 0; color: #666;">🏢 {job['company']} • 📍 {job['location']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if user profile is complete
    if not st.session_state.user_profile.get('name') or not st.session_state.user_profile.get('experience'):
        st.error("⚠️ Please complete your profile first!")
        if st.button("← Go to Profile"):
            st.session_state.show_resume_generator = False
            st.rerun()
        return
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write("**Your Profile:**", st.session_state.user_profile.get('name', 'N/A'))
    
    with col2:
        if st.button("← Back to Jobs"):
            st.session_state.show_resume_generator = False
            st.session_state.generated_resume = None
            st.rerun()
    
    st.markdown("---")
    
    # Generate resume button
    if st.button("🚀 Generate Tailored Resume", type="primary", use_container_width=True):
        with st.spinner("🤖 Creating your personalized resume..."):
            text_gen = get_text_generator()
            resume = text_gen.generate_resume(st.session_state.user_profile, job)
            
            if resume:
                st.session_state.generated_resume = resume
                # Clear the widget state to prevent stale cached values
                if "resume_editor" in st.session_state:
                    del st.session_state.resume_editor
                st.success("✅ Resume generated successfully!")
                st.balloons()
                # Rerun to update the UI with the generated resume
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ Failed to generate resume. Please try again.")
    
    # Display generated resume
    if st.session_state.generated_resume:
        st.markdown("---")
        st.subheader("📋 Your Tailored Resume")
        
        # Display resume in a text area for editing
        edited_resume = st.text_area(
            "You can edit the resume below:",
            value=st.session_state.generated_resume,
            height=600,
            key="resume_editor"
        )
        
        # Update if edited (only if the edited value is actually different from current)
        # This prevents overwriting with stale cached values
        if edited_resume != st.session_state.generated_resume:
            st.session_state.generated_resume = edited_resume
        
        # Download buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download as TXT
            st.download_button(
                label="📥 Download as TXT",
                data=st.session_state.generated_resume,
                file_name=f"resume_{job['company']}_{job['title']}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            # Copy to clipboard button
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.code(st.session_state.generated_resume, language=None)
                st.info("Select and copy the text above")
        
        with col3:
            # Apply to job button
            if job['url'] != '#':
                st.link_button(
                    "🚀 Apply to Job",
                    job['url'],
                    use_container_width=True,
                    type="primary"
                )

def main():
    # Check if resume generator should be shown
    if st.session_state.get('show_resume_generator', False):
        display_resume_generator()
        return
    
    st.markdown('<h1 class="main-header">🔍 Semantic Job Search & Resume Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered job matching with personalized resume generation</p>', unsafe_allow_html=True)
    
    # Add tabs for different sections
    tab1, tab2 = st.tabs(["🔍 Job Search", "👤 My Profile"])
    
    with tab2:
        display_user_profile()
    
    with tab1:
        with st.sidebar:
            st.header("⚙️ Search Settings")
            
            search_query = st.text_input("🔎 Keywords", value="software developer")
            location = st.text_input("📍 Location", value="Hong Kong")
            
            col1, col2 = st.columns(2)
            with col1:
                country = st.selectbox("🌍 Country", ["hk", "us", "uk", "sg", "au", "ca"])
            with col2:
                job_type = st.selectbox("⏰ Type", ["fulltime", "parttime", "contract", "temporary", "internship"])
            
            max_rows = st.slider("📊 Max Jobs", 5, 15, 15, 5)
            
            st.divider()
            fetch_jobs = st.button("🔄 Fetch Jobs", type="primary", use_container_width=True)
            st.divider()
            
            if st.session_state.jobs_cache:
                cache_info = st.session_state.jobs_cache
                st.metric("📦 Cached Jobs", cache_info.get('count', 0))
                st.caption(f"🕒 {cache_info.get('timestamp', 'Never')}")
                
                if st.button("🗑️ Clear"):
                    st.session_state.jobs_cache = {}
                    st.rerun()
        
        if fetch_jobs:
            scraper = get_job_scraper()
            with st.spinner("🔄 Fetching..."):
                jobs = scraper.search_jobs(search_query, location, max_rows, job_type, country)
            
            if jobs:
                st.session_state.jobs_cache = {
                    'jobs': jobs,
                    'count': len(jobs),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'query': search_query
                }
                st.success(f"✅ Fetched {len(jobs)} jobs!")
                st.balloons()
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ No jobs found")
        
        if not st.session_state.jobs_cache:
            st.info("👆 Click 'Fetch Jobs' to start")
            return
        
        jobs = st.session_state.jobs_cache['jobs']
        
        st.markdown("---")
        
        # Automatic job matching based on uploaded resume or profile
        has_resume = st.session_state.resume_text is not None
        has_profile = (st.session_state.user_profile.get('summary') or 
                      st.session_state.user_profile.get('experience') or 
                      st.session_state.user_profile.get('skills'))
        
        if has_resume or has_profile:
            st.header("🎯 Automatic Job Matching")
            if has_resume:
                st.info("💡 We'll automatically find the best matching jobs based on your uploaded resume!")
            else:
                st.info("💡 We'll automatically find the best matching jobs based on your profile!")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if has_resume:
                    st.write("**Resume-based matching will analyze your skills, experience, and qualifications to find the best fit jobs.**")
                else:
                    st.write("**Profile-based matching will analyze your skills, experience, and qualifications to find the best fit jobs.**")
            
            with col2:
                num_results_auto = st.number_input("Results", 1, len(jobs), min(10, len(jobs)), key="auto_results")
                min_score_auto = st.slider("Min score", 0.0, 1.0, 0.0, 0.05, key="auto_min_score")
            
            match_button = st.button("🎯 Find Best Matching Jobs", type="primary", use_container_width=True, key="auto_match")
            
            if match_button:
                embedding_gen = get_embedding_generator()
                search_engine = SemanticJobSearch(embedding_gen)
                search_engine.index_jobs(jobs)
                
                # Create a comprehensive query from resume text or profile
                if has_resume:
                    resume_query = st.session_state.resume_text
                    # If we have structured profile, enhance the query
                    if st.session_state.user_profile.get('summary'):
                        profile_data = f"{st.session_state.user_profile.get('summary', '')} {st.session_state.user_profile.get('experience', '')} {st.session_state.user_profile.get('skills', '')}"
                        resume_query = f"{resume_query} {profile_data}"
                else:
                    # Use profile data to create query
                    resume_query = f"{st.session_state.user_profile.get('summary', '')} {st.session_state.user_profile.get('experience', '')} {st.session_state.user_profile.get('skills', '')} {st.session_state.user_profile.get('education', '')}"
                
                with st.spinner("🤖 Analyzing your profile and matching jobs..."):
                    results = search_engine.search(resume_query, top_k=num_results_auto)
                
                results = [r for r in results if r['similarity_score'] >= min_score_auto]
                st.session_state.matched_jobs = results
                
                st.markdown("---")
                
                if results:
                    st.success(f"✅ Found {len(results)} matching jobs based on your profile!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Avg Match", f"{np.mean([r['similarity_score'] for r in results]):.1%}")
                    with col2:
                        st.metric("Best Match", f"{results[0]['similarity_score']:.1%}")
                    with col3:
                        st.metric("Total Jobs", len(results))
                    
                    st.markdown("---")
                    
                    for i, result in enumerate(results, 1):
                        display_job_card(result, i)
                else:
                    st.warning("No matching jobs found. Try adjusting the minimum score or fetch more jobs.")
            
            # Display previously matched jobs if available
            elif st.session_state.matched_jobs:
                st.info(f"💡 Showing {len(st.session_state.matched_jobs)} previously matched jobs. Click 'Find Best Matching Jobs' to refresh.")
                st.markdown("---")
                
                for i, result in enumerate(st.session_state.matched_jobs, 1):
                    display_job_card(result, i)
            
            st.markdown("---")
            st.markdown("---")
        
        st.header("🎯 Manual Semantic Search")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            user_query = st.text_area(
                "Describe your ideal job",
                height=150,
                placeholder="Python developer with ML experience...",
                key="manual_search"
            )
        
        with col2:
            st.write("")
            st.write("")
            num_results = st.number_input("Results", 1, len(jobs), min(10, len(jobs)), key="manual_results")
            st.write("")
            min_score = st.slider("Min score", 0.0, 1.0, 0.0, 0.05, key="manual_min_score")
        
        search_button = st.button("🔍 Search", type="primary", use_container_width=True, key="manual_search_btn")
        
        if search_button and user_query:
            embedding_gen = get_embedding_generator()
            search_engine = SemanticJobSearch(embedding_gen)
            search_engine.index_jobs(jobs)
            
            with st.spinner("🤖 Analyzing..."):
                results = search_engine.search(user_query, top_k=num_results)
            
            results = [r for r in results if r['similarity_score'] >= min_score]
            
            st.markdown("---")
            
            if results:
                st.success(f"✅ Found {len(results)} jobs!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Avg", f"{np.mean([r['similarity_score'] for r in results]):.1%}")
                with col2:
                    st.metric("Best", f"{results[0]['similarity_score']:.1%}")
                with col3:
                    st.metric("Total", len(results))
                
                st.markdown("---")
                
                for i, result in enumerate(results, 1):
                    display_job_card(result, i)
            else:
                st.warning("No matches")
        
        elif search_button:
            st.warning("⚠️ Enter a query!")

if __name__ == "__main__":
    main()
