# Application Flow Diagram

## 🎯 User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                    FIRST TIME USER FLOW                          │
└─────────────────────────────────────────────────────────────────┘

1️⃣  Launch App
    └─> streamlit run app.py
        └─> Opens at localhost:8501

2️⃣  Create Profile (My Profile Tab)
    ├─> Fill Personal Info
    │   ├─> Name, Email, Phone, Location
    │   └─> LinkedIn, Portfolio
    ├─> Add Professional Summary
    ├─> Enter Work Experience
    ├─> Add Education
    ├─> List Skills
    └─> Include Certifications
        └─> Click "Save Profile" ✅

3️⃣  Search Jobs (Job Search Tab)
    ├─> Enter Keywords (e.g., "Python Developer")
    ├─> Set Location
    ├─> Choose Country & Job Type
    └─> Click "Fetch Jobs" 🔄
        └─> Jobs Retrieved from Indeed ✅

4️⃣  Find Best Matches
    ├─> Describe Ideal Job in Detail
    ├─> Set Number of Results
    ├─> Set Minimum Match Score
    └─> Click "Search" 🔍
        └─> AI Ranks Jobs by Relevance ✅

5️⃣  Generate Resume
    ├─> Click "📄 Resume" on Desired Job
    ├─> Review Job Details
    └─> Click "Generate Tailored Resume" 🚀
        └─> AI Creates Custom Resume ✅

6️⃣  Finalize & Apply
    ├─> Review Generated Resume
    ├─> Edit if Needed
    ├─> Download as TXT 📥
    └─> Click "Apply to Job" 🚀
        └─> Opens Job Posting ✅
```

---

## 🔄 Returning User Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    RETURNING USER FLOW                           │
└─────────────────────────────────────────────────────────────────┘

1️⃣  Launch App
    └─> Profile Already Saved ✅

2️⃣  Search New Jobs
    └─> Repeat steps 3️⃣-6️⃣ from above

OR

2️⃣  Update Profile
    ├─> Go to My Profile Tab
    ├─> Edit Information
    └─> Save Changes
        └─> Use Updated Profile for New Resumes
```

---

## 🏗️ Technical Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   Browser    │
│  (Streamlit) │
└──────┬───────┘
       │
       ├─> SESSION STATE
       │   ├─> user_profile: {}
       │   ├─> jobs_cache: {}
       │   ├─> generated_resume: ""
       │   └─> embedding_gen: API
       │
       ├─> JOB SEARCH FLOW
       │   │
       │   ├─> RapidAPI (Indeed Scraper)
       │   │   └─> Fetch Job Listings
       │   │       └─> Return: Title, Company, Description, Skills
       │   │
       │   ├─> Azure OpenAI (Embeddings)
       │   │   ├─> Embed Job Descriptions
       │   │   └─> Embed User Query
       │   │       └─> Return: Vector Embeddings
       │   │
       │   └─> Scikit-learn
       │       └─> Cosine Similarity
       │           └─> Return: Ranked Jobs with Scores
       │
       └─> RESUME GENERATION FLOW
           │
           ├─> User Profile + Job Description
           │   └─> Combine Data
           │
           └─> Azure OpenAI (GPT-4)
               ├─> Generate Tailored Resume
               │   └─> Emphasize Relevant Skills
               │   └─> Include Job Keywords
               │   └─> ATS Optimization
               │
               └─> Return: Formatted Resume Text
```

---

## 📊 Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA FLOW DIAGRAM                             │
└─────────────────────────────────────────────────────────────────┘

USER INPUT                 PROCESSING                OUTPUT
──────────                ───────────               ────────

Keywords/Location    →    Indeed API        →    Job Listings
                                                      ↓
Job Descriptions     →    Azure Embeddings  →    Vectors
                              +                      ↓
User Query          →    Azure Embeddings  →    Vector
                              ↓                      ↓
                         Cosine Similarity    →  Match Scores
                                                      ↓
                                                 Ranked Jobs
                                                      ↓
Selected Job         →         +             →       ↓
      +                        ↓                     ↓
User Profile         →    Azure GPT-4       →  Tailored Resume
                                                      ↓
                                                  Download
                                                      ↓
                                                   Apply!
```

---

## 🎨 UI Component Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    UI COMPONENT TREE                             │
└─────────────────────────────────────────────────────────────────┘

App Root
│
├─> Header
│   ├─> Title: "Semantic Job Search & Resume Generator"
│   └─> Subtitle: "AI-powered job matching..."
│
├─> Navigation Check
│   └─> if show_resume_generator:
│       └─> display_resume_generator()
│   └─> else:
│       └─> Main Interface
│
├─> Main Interface
│   │
│   ├─> Tab 1: Job Search
│   │   │
│   │   ├─> Sidebar
│   │   │   ├─> Search Settings
│   │   │   ├─> Filters
│   │   │   ├─> Fetch Button
│   │   │   └─> Cache Info
│   │   │
│   │   └─> Main Content
│   │       ├─> Semantic Search Input
│   │       ├─> Search Button
│   │       └─> Results Section
│   │           └─> Job Cards
│   │               ├─> Job Details
│   │               ├─> Match Score
│   │               ├─> Benefits/Skills
│   │               └─> Buttons
│   │                   ├─> Apply
│   │                   └─> Resume
│   │
│   └─> Tab 2: My Profile
│       └─> Profile Form
│           ├─> Personal Info Section
│           ├─> Summary Section
│           ├─> Experience Section
│           ├─> Education Section
│           ├─> Skills Section
│           ├─> Certifications Section
│           └─> Save Button
│
└─> Resume Generator Page
    ├─> Selected Job Display
    ├─> Back Button
    ├─> Generate Button
    └─> Resume Section
        ├─> Editable Text Area
        └─> Action Buttons
            ├─> Download
            ├─> Copy
            └─> Apply
```

---

## 🔐 State Management

```
┌─────────────────────────────────────────────────────────────────┐
│                    SESSION STATE VARIABLES                       │
└─────────────────────────────────────────────────────────────────┘

st.session_state = {
    'search_history': [],           // Historical searches
    'jobs_cache': {                 // Cached job listings
        'jobs': [...],              // Job objects array
        'count': 15,                // Number of jobs
        'timestamp': "2024-...",    // When fetched
        'query': "software dev"     // Search query used
    },
    'embedding_gen': API_Instance,  // Embedding API (cached)
    'user_profile': {               // User information
        'name': "John Doe",
        'email': "john@email.com",
        'phone': "+1-234-567-8900",
        'location': "New York",
        'linkedin': "linkedin.com/...",
        'portfolio': "example.com",
        'summary': "Experienced...",
        'experience': "Senior...",
        'education': "B.S. in...",
        'skills': "Python, JS...",
        'certifications': "AWS..."
    },
    'generated_resume': "...",      // Latest resume text
    'text_gen': API_Instance,       // Text gen API (cached)
    'selected_job': {...},          // Job for resume gen
    'show_resume_generator': false  // Navigation flag
}
```

---

## 🎯 Key Interactions

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERACTIONS                             │
└─────────────────────────────────────────────────────────────────┘

Action                          Trigger                Result
──────                          ───────               ──────

Save Profile          →    Form Submit Button   →   Update session_state
                                                     Show success message

Fetch Jobs           →    Fetch Jobs Button    →   API call to Indeed
                                                     Cache results
                                                     Show job count

Semantic Search      →    Search Button        →   Generate embeddings
                                                     Calculate similarities
                                                     Display ranked results

Generate Resume      →    Resume Button        →   Navigate to generator
                          Generate Button            Call GPT API
                                                     Display result

Download Resume      →    Download Button      →   Create TXT file
                                                     Trigger browser download

Apply to Job         →    Apply Button         →   Open job URL
                                                     (in new tab)

Navigate Back        →    Back Button          →   Clear resume state
                                                     Return to job list
```

---

## 🚀 Performance Optimizations

```
┌─────────────────────────────────────────────────────────────────┐
│                    OPTIMIZATION STRATEGIES                       │
└─────────────────────────────────────────────────────────────────┘

1. API Instance Caching
   ├─> Embedding generator: Created once, reused
   └─> Text generator: Created once, reused

2. Job Caching
   ├─> Fetch once, use multiple times
   ├─> Cache includes timestamp
   └─> Manual clear option available

3. Batch Processing
   ├─> Embeddings generated in batches of 10
   ├─> Progress bar for user feedback
   └─> Reduces API calls

4. Lazy Loading
   ├─> Resume generator loads on demand
   ├─> APIs initialized when needed
   └─> Components render progressively

5. Session State
   ├─> All data in memory
   ├─> No database queries
   └─> Instant access to cached data
```

---

## 🎓 Best Practices Implemented

```
┌─────────────────────────────────────────────────────────────────┐
│                    DESIGN PATTERNS USED                          │
└─────────────────────────────────────────────────────────────────┘

✅ Singleton Pattern
   └─> API instances cached in session state

✅ Factory Pattern
   └─> Helper functions create API instances

✅ MVC Pattern
   └─> Separation: Data (state) / Logic (classes) / View (display)

✅ Progressive Disclosure
   └─> Complex features hidden until needed

✅ Defensive Programming
   └─> Null checks, error handling, user feedback

✅ DRY (Don't Repeat Yourself)
   └─> Reusable display functions

✅ Modular Architecture
   └─> Each feature in separate function

✅ Consistent UI/UX
   └─> Similar patterns across all pages
```

---

This flow diagram provides a comprehensive view of how the application works from both user and technical perspectives. Use it as a reference for understanding the system architecture and user experience design.
