# Technical Operations Flow - Implementation Verification

This document verifies that the implementation aligns with the technical operations table.

## Flow Overview

### Original Flow (High Load) → Midpoint Flow (Load Managed)

| Technical Operation | Original Flow | Midpoint Flow | Implementation Status |
|---------------------|---------------|---------------|----------------------|
| **Profile Extraction (GPT-4o)** | Triggered by Upload | **Unchanged (Necessary)** | ✅ Implemented |
| **Job Fetch (Indeed API)** | Triggered by Analyze | **Isolated and Gated** | ✅ Implemented |
| **Embedding Generation** | Triggered immediately after Fetch | **Delayed and Gated** | ✅ Implemented |
| **Rate Limit Management** | High concentration in one burst | **Separates bursts** | ✅ Implemented |
| **UX Improvement** | User waits 15-20 seconds | **5s for titles, then 10-15s when ready** | ✅ Implemented |

---

## Step-by-Step Implementation

### Step 0: Profile Extraction (GPT-4o)
**Location:** `hooks/useFileUpload.js` → `services/api.js::extractProfile()`

**Technical Operation:**
- ✅ **Triggered by Upload**: Automatically called after resume upload
- ✅ **Unchanged**: Remains the first required AI call
- ✅ **Necessary**: Must happen before any job analysis

**Implementation:**
```javascript
// In useFileUpload.js (line 60)
const profile = await ApiService.extractProfile(result.id);
```

**API Endpoint:** `POST /api/resume/{resumeId}/extract`

---

### Step 1: Fetch Market Jobs
**Location:** `components/DashboardLayout.jsx::handleFetchJobs()` → `services/api.js::fetchJobs()`

**Technical Operations:**

#### 1.1 Job Fetch (Indeed API)
- ✅ **Isolated and Gated**: Triggered by "Fetch Market Jobs" button
- ✅ **NO Embedding Generation**: This endpoint only calls Indeed API
- ✅ **Rate Limit Management**: Small burst of API calls (just Indeed API)
- ✅ **UX**: User waits ~5 seconds for job titles

**Implementation:**
```javascript
// Step 1: Fetch jobs from Indeed (NO embeddings - just raw job data)
const jobsResult = await ApiService.fetchJobs(filters);
```

**API Endpoint:** `POST /api/jobs/fetch`

**What it does:**
- Calls Indeed Scraper API via RapidAPI
- Returns raw job listings (title, company, location, URL)
- **Does NOT** call Azure Embedding API
- **Does NOT** perform semantic indexing

#### 1.2 Market Positioning (GPT-4o)
- ✅ **Based on resume only**: NOT job list
- ✅ **Uses GPT-4o**: For resume analysis
- ✅ **Does NOT trigger job embeddings**: That's only in Step 2

**Implementation:**
```javascript
// Get market positioning based on resume only (NOT job list)
// This uses GPT-4o for resume analysis but does NOT trigger job embeddings
const positioning = await ApiService.getMarketPositioning(profileData, filters);
```

**API Endpoint:** `POST /api/market/positioning`

**What it does:**
- Analyzes user's resume/profile using GPT-4o
- Generates market insights (salary band, skill gaps, accreditations)
- **Does NOT** analyze job listings
- **Does NOT** generate job embeddings

---

### Step 2: Analyze and Rank Top 15 Matches
**Location:** `components/DashboardLayout.jsx::handleAnalyze()` → `services/api.js::getJobMatches()`

**Technical Operations (High Load):**

#### 2.1 Embedding Generation
- ✅ **Delayed and Gated**: Only triggered by "Analyze and Rank Top 15 Matches" button
- ✅ **Semantic Indexing**: Job Embeddings via Azure OpenAI
- ✅ **Rate Limit Management**: Second burst of API calls (Azure Embedding API)
- ✅ **UX**: User commits to 10-15 second AI analysis only when ready

**Implementation:**
```javascript
// Step 2: Expensive AI processing - THIS is where embeddings happen
// 1. Semantic Indexing (Job Embeddings via Azure OpenAI)
// 2. Semantic Search (Cosine Similarity)
// 3. Skill Matching
const matches = await ApiService.getJobMatches(profileData, filters, 15);
```

**API Endpoint:** `POST /api/jobs/matches`

**What it does:**
1. **Semantic Indexing**: Generates embeddings for all fetched jobs (Azure OpenAI Embeddings API)
2. **Semantic Search**: Performs cosine similarity matching between resume and jobs
3. **Skill Matching**: Detailed skill overlap analysis
4. **Ranking**: Returns top 15 matches sorted by relevance

**This is the ONLY place where job embeddings are generated.**

---

## Rate Limit Management

### Original Flow (High Load)
```
Upload → Profile Extract → [BURST: Job Fetch + Embeddings + Ranking] → Results
         (GPT-4o)         (15-20 seconds of API calls)
```

### Midpoint Flow (Load Managed)
```
Upload → Profile Extract → [BURST 1: Job Fetch] → [User Reviews] → [BURST 2: Embeddings + Ranking] → Results
         (GPT-4o)         (~5 seconds)          (User decides)   (10-15 seconds)
```

**Benefits:**
- ✅ Separates API bursts into two smaller operations
- ✅ User gets immediate feedback (job titles) before committing to expensive analysis
- ✅ Reduces risk of rate limiting by spacing out API calls
- ✅ Better UX: User can review jobs before triggering expensive operations

---

## UX Improvement

### Original Flow
- User clicks "Analyze"
- Waits 15-20 seconds for everything
- Gets results (or timeout/error)

### Midpoint Flow
- User clicks "Fetch Market Jobs"
- Waits ~5 seconds for job titles and market profile
- **User reviews results**
- User clicks "Analyze and Rank Top 15 Matches" (only if interested)
- Waits 10-15 seconds for AI-powered ranking
- Gets ranked results

**Key Improvement:** User can see job titles immediately and decide if they want to proceed with expensive AI analysis.

---

## API Endpoints Summary

| Endpoint | Method | Purpose | Triggers Embeddings? | Rate Limit Impact |
|----------|--------|---------|---------------------|-------------------|
| `/api/resume/upload` | POST | Upload resume file | ❌ No | Low |
| `/api/resume/{id}/extract` | POST | Extract profile (GPT-4o) | ❌ No | Medium (GPT-4o) |
| `/api/jobs/fetch` | POST | Fetch jobs from Indeed | ❌ No | Medium (Indeed API) |
| `/api/market/positioning` | POST | Market analysis (GPT-4o) | ❌ No | Medium (GPT-4o) |
| `/api/jobs/matches` | POST | AI-powered ranking | ✅ **YES** | High (Azure Embeddings) |

---

## Verification Checklist

- [x] Profile extraction triggered by upload (unchanged)
- [x] Job fetch isolated and gated (separate button)
- [x] Embedding generation delayed and gated (separate button)
- [x] Rate limit management separates bursts
- [x] UX improvement: 5s wait for titles, then 10-15s when ready
- [x] Market positioning based on resume only (not job list)
- [x] No embeddings generated in Step 1
- [x] Embeddings only generated in Step 2

---

## Code Locations

- **Profile Extraction**: `hooks/useFileUpload.js:60` → `services/api.js:extractProfile()`
- **Job Fetch (Step 1)**: `components/DashboardLayout.jsx:handleFetchJobs()` → `services/api.js:fetchJobs()`
- **Market Positioning**: `components/DashboardLayout.jsx:handleFetchJobs()` → `services/api.js:getMarketPositioning()`
- **AI Ranking (Step 2)**: `components/DashboardLayout.jsx:handleAnalyze()` → `services/api.js:getJobMatches()`

---

## Notes for Backend Implementation

The backend should implement these endpoints with the following behavior:

1. **`/api/jobs/fetch`**: 
   - Only calls Indeed Scraper API
   - Returns raw job data
   - **MUST NOT** call Azure Embedding API
   - **MUST NOT** perform semantic indexing

2. **`/api/market/positioning`**:
   - Uses GPT-4o to analyze resume/profile
   - Generates market insights
   - **MUST NOT** analyze job listings
   - **MUST NOT** generate job embeddings

3. **`/api/jobs/matches`**:
   - **MUST** generate job embeddings (Azure OpenAI)
   - **MUST** perform semantic search
   - **MUST** perform skill matching
   - Returns top 15 ranked matches
