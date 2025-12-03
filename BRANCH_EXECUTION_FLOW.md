# Branch Execution Flow - How This Branch Runs

## Overview

This branch contains **two separate applications** that can run independently:

1. **React/Vite Frontend** - Modern React application (Port 3000)
2. **Streamlit Backend** - Python Streamlit application (Port 8501)

The React frontend expects a **REST API backend** (Port 8000), which may or may not exist yet.

---

## 🚀 How to Run

### Option 1: React Frontend (Recommended for Development)

**Prerequisites:**
- Node.js and npm installed
- `.env` file configured (see `.env.example`)

**Steps:**
```bash
# 1. Install dependencies
npm install

# 2. Configure environment variables
# Copy .env.example to .env and fill in your API keys
cp .env.example .env

# 3. Start the development server
npm run dev
# or
npm start
```

**What happens:**
- Vite dev server starts on **port 3000** (configurable in `vite.config.js`)
- Opens browser automatically at `http://localhost:3000`
- React app loads from `index.html` → `src/main.jsx` → `App.jsx`
- App renders `DashboardLayout` component

**Configuration:**
- API URL: Set via `REACT_APP_API_URL` in `.env` (default: `http://localhost:8000/api`)
- Mock API: Set `REACT_APP_USE_MOCK_API=true` to use mock data (no backend needed)
- If `USE_MOCK_API=false` and no backend on port 8000, API calls will fail but app still loads

---

### Option 2: Streamlit Backend (Standalone Application)

**Prerequisites:**
- Python 3.8+ installed
- Dependencies installed: `pip install -r requirements.txt`
- `.streamlit/secrets.toml` configured (see `.streamlit/secrets.toml.example`)

**Steps:**
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Configure secrets
# Copy secrets.toml.example to secrets.toml and add your API keys
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your keys

# 3. Run Streamlit app
streamlit run app.py
```

**What happens:**
- Streamlit server starts on **port 8501** (default)
- Opens browser automatically at `http://localhost:8501`
- Full-featured job search and resume generation application
- Uses Azure OpenAI for embeddings and GPT-4 for resume generation
- Uses RapidAPI for Indeed job scraping

**Note:** This is a **separate application** from the React frontend. They don't communicate with each other.

---

## 📁 Project Structure

```
/workspace/
├── App.jsx                    # React app entry point
├── src/
│   └── main.jsx              # React DOM mounting point
├── components/
│   ├── DashboardLayout.jsx   # Main dashboard component
│   ├── Sidebar.jsx           # Sidebar with controls
│   ├── JobList.jsx           # Job listings display
│   └── JobMatchTable.jsx     # Ranked matches table
├── services/
│   ├── api.js                # API service (calls backend)
│   └── mockApi.js           # Mock API for development
├── config/
│   └── api.config.js        # API configuration
├── hooks/
│   ├── useFileUpload.js     # File upload hook
│   └── useToast.js          # Toast notifications
├── app.py                    # Streamlit application (separate)
├── package.json              # Node.js dependencies
├── vite.config.js           # Vite configuration
└── requirements.txt         # Python dependencies
```

---

## 🔄 Execution Flow

### React Frontend Flow

```
1. User opens browser → http://localhost:3000
   ↓
2. index.html loads
   ↓
3. src/main.jsx executes
   - Creates React root
   - Renders <App /> with ErrorBoundary
   ↓
4. App.jsx renders
   - Manages dark mode state
   - Renders <DashboardLayout />
   ↓
5. DashboardLayout.jsx renders
   - Shows sidebar (Sidebar component)
   - Shows main content area
   - Manages state: profileData, jobs, matches
   ↓
6. User interactions:
   
   a) Upload Resume
      → useFileUpload hook
      → POST /api/resume/upload
      → POST /api/resume/{id}/extract (auto)
      → Profile extracted and stored
   
   b) Fetch Market Jobs
      → handleFetchJobs()
      → POST /api/jobs/fetch
      → Raw jobs displayed
      → POST /api/market/positioning (auto)
      → Market insights displayed
   
   c) Analyze and Rank
      → handleAnalyze()
      → POST /api/jobs/matches
      → Embeddings generated (Azure OpenAI)
      → Semantic search performed
      → Top 15 matches displayed
   
   d) Generate Tailored Resume
      → handleTailorResume()
      → POST /api/resume/tailor
      → GPT-4 generates resume
      → Resume downloaded/displayed
```

### Streamlit Backend Flow

```
1. User runs: streamlit run app.py
   ↓
2. Streamlit server starts on port 8501
   ↓
3. main() function executes
   ↓
4. Session state initialized
   - jobs_cache, user_profile, embedding_gen, etc.
   ↓
5. UI rendered with tabs:
   - "Job Search" tab
   - "My Profile" tab
   ↓
6. User interactions:
   
   a) Upload Resume (My Profile tab)
      → extract_text_from_resume()
      → extract_profile_from_resume() (GPT-4o)
      → Profile auto-filled
   
   b) Fetch Jobs (Job Search tab)
      → IndeedScraperAPI.search_jobs()
      → Jobs cached in session_state
   
   c) Semantic Search
      → SemanticJobSearch.index_jobs() (embeddings)
      → SemanticJobSearch.search() (cosine similarity)
      → Ranked results displayed
   
   d) Generate Resume
      → AzureOpenAITextGenerator.generate_resume()
      → Match score calculated
      → Resume displayed and downloadable
```

---

## 🔌 API Endpoints (Expected by React Frontend)

The React frontend expects these REST API endpoints at `http://localhost:8000/api`:

| Endpoint | Method | Purpose | When Called |
|----------|--------|---------|-------------|
| `/api/resume/upload` | POST | Upload resume file | On file upload |
| `/api/resume/{id}/extract` | POST | Extract profile from resume | Auto after upload |
| `/api/jobs/fetch` | POST | Fetch jobs from Indeed | "Fetch Market Jobs" button |
| `/api/market/positioning` | POST | Get market insights | Auto after job fetch |
| `/api/jobs/matches` | POST | Get AI-ranked job matches | "Analyze and Rank" button |
| `/api/resume/tailor` | POST | Generate tailored resume | "Generate Resume" button |

**Note:** These endpoints are **NOT** provided by the Streamlit app. You need a separate REST API backend (Flask/FastAPI) or use the mock API.

---

## 🎯 Two-Step User Flow (React Frontend)

The React frontend implements a **two-step process** to manage API rate limits:

### Step 1: Fetch Market Jobs
- **Button:** "Fetch Market Jobs"
- **Operations:**
  1. Fetches jobs from Indeed API (via RapidAPI)
  2. Gets market positioning analysis (GPT-4o on resume only)
- **Time:** ~5 seconds
- **No embeddings generated** (saves API calls)

### Step 2: Analyze and Rank
- **Button:** "Analyze and Rank Top 15 Matches"
- **Operations:**
  1. Generates embeddings for all jobs (Azure OpenAI)
  2. Performs semantic search (cosine similarity)
  3. Ranks top 15 matches
- **Time:** ~10-15 seconds
- **Only triggered when user is ready**

**Benefits:**
- User sees job titles immediately
- User decides if they want expensive AI analysis
- Separates API bursts to avoid rate limits

---

## 🔧 Configuration

### React Frontend Configuration (`.env`)

```bash
# Backend API URL
REACT_APP_API_URL=http://localhost:8000/api

# Use Mock API (true = use mock data, false = use real backend)
REACT_APP_USE_MOCK_API=true

# API Keys (optional, if backend needs them)
REACT_APP_AZURE_OPENAI_API_KEY=your-key
REACT_APP_AZURE_OPENAI_ENDPOINT=https://your-endpoint
REACT_APP_RAPIDAPI_KEY=your-key
REACT_APP_BACKEND_API_KEY=your-key
```

### Streamlit Configuration (`.streamlit/secrets.toml`)

```toml
AZURE_OPENAI_API_KEY = "your-key"
AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com"
RAPIDAPI_KEY = "your-key"
```

---

## 🚦 Current Status

### What Works:
- ✅ React frontend can run independently (with mock API)
- ✅ Streamlit backend can run independently
- ✅ Both applications are functional

### What's Missing:
- ❌ REST API backend on port 8000 (needed for React frontend to use real APIs)
- ⚠️ React frontend and Streamlit backend don't communicate

### Options:
1. **Use Mock API:** Set `REACT_APP_USE_MOCK_API=true` - React app works with fake data
2. **Build REST API Backend:** Create Flask/FastAPI server on port 8000 that implements the endpoints
3. **Use Streamlit Only:** Run `streamlit run app.py` for full functionality

---

## 📊 Key Differences

| Feature | React Frontend | Streamlit Backend |
|---------|---------------|-------------------|
| **Port** | 3000 | 8501 |
| **Technology** | React + Vite | Python + Streamlit |
| **UI Framework** | React Components | Streamlit Widgets |
| **API Communication** | REST API (port 8000) | Direct Python calls |
| **State Management** | React useState/useEffect | Streamlit session_state |
| **File Upload** | React hooks | Streamlit file_uploader |
| **Deployment** | Vercel/Netlify/GitHub Pages | Streamlit Cloud |

---

## 🎓 Development Workflow

### For React Frontend Development:
```bash
# Terminal 1: React dev server
npm run dev

# Terminal 2: Backend API (if you have one)
# python backend_server.py  # or similar
```

### For Streamlit Development:
```bash
# Single terminal
streamlit run app.py
```

---

## 🔍 Troubleshooting

### React App Shows Blank Page:
- Check browser console for JavaScript errors
- Verify `src/main.jsx` is mounting correctly
- Check that `App.jsx` and `DashboardLayout.jsx` exist

### API Calls Fail:
- If `USE_MOCK_API=false`: Backend must be running on port 8000
- If `USE_MOCK_API=true`: Should work without backend
- Check `.env` file configuration

### Streamlit App Errors:
- Verify `.streamlit/secrets.toml` exists and has API keys
- Check `requirements.txt` dependencies are installed
- Review Streamlit console for error messages

---

## 📝 Summary

**This branch runs in two ways:**

1. **React Frontend (Port 3000):**
   - Modern React application
   - Requires REST API backend (port 8000) OR uses mock API
   - Two-step process: Fetch Jobs → Analyze and Rank
   - Better UX with separated API calls

2. **Streamlit Backend (Port 8501):**
   - Complete standalone application
   - All functionality built-in
   - No separate backend needed
   - Traditional Streamlit UI

**They are separate applications** - choose one based on your needs!
