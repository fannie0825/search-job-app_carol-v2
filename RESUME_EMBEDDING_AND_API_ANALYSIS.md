# Resume Embedding & API Usage Analysis

## 1. Resume Extraction & Embedding Path

### Current Implementation Flow

#### Step 1: Resume Upload & Text Extraction
- **Location**: `app.py` lines 2755-2765
- **Process**: 
  - User uploads PDF/DOCX/TXT resume
  - `extract_text_from_resume()` extracts raw text
  - Text is stored in `st.session_state.resume_text`

#### Step 2: Resume Embedding Generation
- **Location**: `app.py` lines 2042-2074 (`generate_and_store_resume_embedding()`)
- **Method**: **Vector Embedding (AI-based)**
- **API Used**: Azure OpenAI `text-embedding-3-small` model
- **When Generated**: 
  - Once when resume is uploaded (line 2765)
  - Stored in `st.session_state.resume_embedding` for reuse
- **Embedding Content**: 
  - Combines resume text + user profile (summary, experience, skills)
  - Creates a semantic vector representation

#### Step 3: Skill Prioritization & Matching
- **Location**: `app.py` lines 1793-1868 (`calculate_skill_match()`)
- **Method**: **Semantic Vector Matching (Primary) + String Matching (Fallback)**
- **Process**:
  1. **Semantic Matching** (lines 1807-1846):
     - Generates embeddings for user skills AND job skills separately
     - Uses Azure OpenAI `text-embedding-3-small` for both
     - Calculates cosine similarity between skill embeddings
     - Threshold: 70% similarity required for a match
     - Recognizes related skills (e.g., "JavaScript" ≈ "JS")
  2. **String Matching Fallback** (lines 1853-1868):
     - Used if semantic matching fails (rate limits, errors)
     - Direct text comparison (case-insensitive)
     - Partial matching supported

### Key Finding: Job Indexing is DISABLED

**⚠️ IMPORTANT**: Line 3584 shows that job embedding/indexing is **currently disabled**:

```python
# search_engine.index_jobs(jobs, max_jobs_to_index=jobs_to_index_limit)  # Disabled to save embedding token costs and avoid Rate Limit 429 errors
```

**What this means**:
- Jobs are NOT being indexed with embeddings
- The `SemanticJobSearch.search()` method (line 3606) will return **empty results** because `self.job_embeddings` is empty (line 1758 checks this)
- The system is currently relying **only on skill-based matching** (lines 3609-3618), not semantic job matching

### Current Ranking System

**Actual Ranking Method** (lines 3610-3618):
1. Jobs are fetched from RapidAPI (Indeed)
2. For each job, `calculate_skill_match()` is called
3. Jobs are sorted by `skill_match_score` (highest first)
4. **NOT using vector similarity between resume and job descriptions**

**Summary**:
- ✅ Resume embedding: **Vector-based (Azure OpenAI)**
- ✅ Skill matching: **Vector-based semantic matching (Azure OpenAI)**
- ❌ Job indexing: **DISABLED** (commented out)
- ❌ Job-resume semantic matching: **NOT WORKING** (no job embeddings)

---

## 2. Job Posting Fetching from API

### When "Analyze Profile & Find Matches" is Clicked

**Location**: `app.py` lines 3446-3624

#### Step 1: Profile Analysis (Azure OpenAI)
- **Lines 3459-3542**: Uses Azure OpenAI GPT to infer:
  - Target domains (e.g., FinTech, Data Analytics)
  - Salary expectations
- **API**: Azure OpenAI (text generation)
- **Rate Limit Risk**: Low (only 2 API calls)

#### Step 2: Job Fetching (RapidAPI)
- **Location**: `app.py` lines 3550-3563
- **Function**: `fetch_jobs_with_cache()` → `IndeedScraperAPI.search_jobs()`
- **API Used**: **RapidAPI Indeed Scraper API**
- **Endpoint**: `https://indeed-scraper-api.p.rapidapi.com/api/job`
- **Method**: POST request
- **Headers**:
  ```python
  'x-rapidapi-host': 'indeed-scraper-api.p.rapidapi.com'
  'x-rapidapi-key': RAPIDAPI_KEY
  ```
- **Parameters**:
  - `maxRows`: 25 (line 3559)
  - `query`: Inferred domains (line 3549)
  - `location`: "Hong Kong"
  - `country`: "hk"

#### Step 3: Retry Logic for 429 Errors
- **Location**: `app.py` lines 1408, 172-250
- **Function**: `api_call_with_retry()`
- **Behavior**:
  - Detects 429 status code
  - Exponential backoff retry (up to 3 retries)
  - Shows user warning messages
  - Returns `None` if all retries fail

### Rate Limit Analysis

**Your Suspicion is CORRECT**: The 429 errors are likely from **RapidAPI**, not OpenAI.

**Evidence**:
1. **RapidAPI Rate Limits**:
   - Free tier: Typically 100-1000 requests/month
   - Paid tiers: Varies by subscription
   - **No built-in rate limit handling** in the code (only retry logic)

2. **OpenAI Rate Limits**:
   - Azure OpenAI has higher limits
   - The code has retry logic that should handle 429s
   - Job embedding generation is **disabled** (line 3584), so fewer OpenAI calls

3. **API Call Pattern**:
   - **RapidAPI**: Called every time "Analyze Profile & Find Matches" is clicked (unless cached)
   - **OpenAI**: 
     - Resume embedding: Once per resume upload
     - Skill matching: Called for each job (could be 25+ calls)
     - Profile inference: 2 calls per button click

### Caching Mechanism

**Job Fetching Cache** (lines 1955-1995):
- **TTL**: 24 hours (line 3554)
- **Cache Key**: Based on query, location, max_rows, job_type, country
- **Purpose**: Avoid hitting RapidAPI rate limits
- **Note**: Cache can be bypassed with `force_refresh=True`

### Potential 429 Error Sources

1. **RapidAPI Indeed Scraper** (Most Likely):
   - Called on every button click (if cache miss)
   - Free tier limits are strict
   - Error shown at line 1426: "Rate limit reached for job search API"

2. **Azure OpenAI Embeddings** (Less Likely):
   - Skill matching generates embeddings for user skills + job skills
   - For 25 jobs with 5 skills each = 25 + 5 = 30 embedding calls
   - Batch processing helps (batch_size=10), but still many calls
   - However, job indexing is disabled, so this is reduced

3. **Azure OpenAI Text Generation** (Unlikely):
   - Only 2 calls per button click (domain + salary inference)
   - Should not hit rate limits

---

## Recommendations

### To Fix 429 Errors:

1. **Check RapidAPI Subscription**:
   - Verify your RapidAPI tier and quota
   - Consider upgrading if on free tier
   - Check RapidAPI dashboard for usage stats

2. **Improve Caching**:
   - Increase cache TTL (currently 24 hours)
   - Add cache for skill embeddings (currently regenerated each time)

3. **Reduce API Calls**:
   - Re-enable job indexing with persistent storage (ChromaDB) to avoid regenerating embeddings
   - Batch skill matching more aggressively
   - Cache skill embeddings per job

4. **Add Rate Limit Detection**:
   - Track RapidAPI calls separately
   - Show specific error messages for RapidAPI vs OpenAI
   - Implement request queuing/throttling

### To Fix Job Matching:

1. **Re-enable Job Indexing** (line 3584):
   - Uncomment the `index_jobs()` call
   - This will enable semantic job-resume matching
   - Use persistent ChromaDB storage to avoid regenerating embeddings

2. **Hybrid Ranking**:
   - Combine semantic similarity (resume-job) + skill matching
   - Weight both scores appropriately

---

## Summary

| Component | Current State | API Used | Rate Limit Risk |
|-----------|---------------|----------|-----------------|
| Resume Embedding | ✅ Working (Vector) | Azure OpenAI | Low |
| Job Indexing | ❌ **DISABLED** | Azure OpenAI | N/A |
| Skill Matching | ✅ Working (Vector) | Azure OpenAI | Medium |
| Job Fetching | ✅ Working | **RapidAPI** | **HIGH** ⚠️ |
| Profile Inference | ✅ Working | Azure OpenAI | Low |

**Most Likely 429 Source**: **RapidAPI Indeed Scraper API** (job fetching)
