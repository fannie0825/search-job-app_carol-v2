# Testing Checklist

Use this checklist to verify all features are working correctly after setup.

## ✅ Pre-Testing Setup

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.streamlit/secrets.toml` file created with valid API keys
- [ ] Azure OpenAI deployments active:
  - [ ] `text-embedding-3-small` (or your embedding model)
  - [ ] `gpt-4o-mini` (or your text generation model)
- [ ] RapidAPI subscription active for Indeed Scraper API

## 🧪 Feature Testing

### 1. Application Launch
- [ ] Run `streamlit run app.py`
- [ ] App opens in browser at localhost:8501
- [ ] No error messages in terminal
- [ ] Main page loads with two tabs visible

### 2. User Profile Management

#### Profile Tab Access
- [ ] Click on "My Profile" tab
- [ ] Profile form is visible
- [ ] All fields are present:
  - [ ] Full Name
  - [ ] Email
  - [ ] Phone
  - [ ] Location
  - [ ] LinkedIn URL
  - [ ] Portfolio/Website
  - [ ] Professional Summary
  - [ ] Work Experience
  - [ ] Education
  - [ ] Skills
  - [ ] Certifications & Awards

#### Profile Creation
- [ ] Fill in all profile fields with test data
- [ ] Click "Save Profile" button
- [ ] Success message appears: "✅ Profile saved successfully!"
- [ ] Page refreshes automatically
- [ ] Return to profile tab - data is still there

#### Profile Editing
- [ ] Modify some fields
- [ ] Click "Save Profile" again
- [ ] Changes are saved
- [ ] Updated data persists

### 3. Job Search Functionality

#### Basic Job Search
- [ ] Switch to "Job Search" tab
- [ ] Sidebar shows "Search Settings"
- [ ] Enter job keywords (e.g., "software developer")
- [ ] Enter location (e.g., "Hong Kong")
- [ ] Select country (e.g., "hk")
- [ ] Select job type (e.g., "fulltime")
- [ ] Adjust max jobs slider (e.g., 15)
- [ ] Click "🔄 Fetch Jobs" button

#### Job Fetching Results
- [ ] Loading spinner appears
- [ ] Jobs are fetched successfully
- [ ] Success message: "✅ Fetched X jobs!"
- [ ] Balloons animation plays
- [ ] Sidebar shows cached jobs count
- [ ] Timestamp is displayed

#### Cache Management
- [ ] Cache information visible in sidebar
- [ ] Click "🗑️ Clear" button
- [ ] Cache is cleared
- [ ] Message prompts to fetch jobs again

### 4. Semantic Search

#### Search Execution
- [ ] Enter detailed query in "Describe your ideal job" field
  - Example: "Python developer with 3+ years experience in machine learning and web development"
- [ ] Adjust number of results
- [ ] Adjust minimum score threshold
- [ ] Click "🔍 Search" button

#### Search Results
- [ ] Indexing progress bar appears
- [ ] "Analyzing..." spinner shows
- [ ] Results are displayed with match percentages
- [ ] Metrics shown: Avg, Best, Total
- [ ] Jobs sorted by relevance
- [ ] Each job card displays:
  - [ ] Job title and rank
  - [ ] Company name and rating
  - [ ] Location
  - [ ] Match score percentage
  - [ ] Job type and salary
  - [ ] Posted date
  - [ ] Benefits (if available)
  - [ ] Skills (if available)
  - [ ] "View Full Description" expandable section
  - [ ] "Apply" button
  - [ ] "📄 Resume" button

### 5. Resume Generation

#### Access Resume Generator
- [ ] Click "📄 Resume" button on any job card
- [ ] Navigate to Resume Generator page
- [ ] Selected job details are displayed:
  - [ ] Job title
  - [ ] Company name
  - [ ] Location

#### Resume Generation Process
- [ ] Profile name is displayed
- [ ] "🚀 Generate Tailored Resume" button is visible
- [ ] Click generate button
- [ ] Loading spinner: "🤖 Creating your personalized resume..."
- [ ] Resume is generated successfully
- [ ] Success message: "✅ Resume generated successfully!"
- [ ] Balloons animation plays

#### Resume Display & Editing
- [ ] Generated resume is displayed in text area
- [ ] Resume includes:
  - [ ] Personal information from profile
  - [ ] Professional summary (tailored)
  - [ ] Work experience (relevant to job)
  - [ ] Education
  - [ ] Skills (matching job requirements)
  - [ ] Proper formatting and sections
- [ ] Resume text is editable
- [ ] Can modify content in text area
- [ ] Changes persist in the editor

#### Resume Actions
- [ ] "📥 Download as TXT" button works
  - [ ] Click button
  - [ ] File downloads with correct name format
  - [ ] File contains resume content
- [ ] "📋 Copy to Clipboard" button works
  - [ ] Click button
  - [ ] Text is displayed for copying
  - [ ] Info message appears
- [ ] "🚀 Apply to Job" button works
  - [ ] Button links to actual job posting
  - [ ] Opens in new tab/window
  - [ ] Correct job URL

#### Navigation
- [ ] "← Back to Jobs" button visible
- [ ] Click back button
- [ ] Returns to job search page
- [ ] Job list is still visible (cached)

### 6. Error Handling

#### Profile Incomplete
- [ ] Clear session state (refresh page)
- [ ] Don't fill profile
- [ ] Try to generate resume
- [ ] Error message: "⚠️ Please complete your profile first!"
- [ ] "← Go to Profile" button appears
- [ ] Click button - navigates to profile tab

#### No Jobs Cached
- [ ] Clear job cache
- [ ] Go to Job Search tab
- [ ] Info message: "👆 Click 'Fetch Jobs' to start"
- [ ] Semantic search section not visible

#### Empty Search Query
- [ ] Leave search query empty
- [ ] Click search button
- [ ] Warning: "⚠️ Enter a query!"

#### API Errors (Intentional Test)
- [ ] Temporarily use invalid API key
- [ ] Try to fetch jobs
- [ ] Error message displays
- [ ] Try to generate resume
- [ ] Error message displays
- [ ] Restore valid API key

### 7. UI/UX Elements

#### Visual Design
- [ ] Main header displays correctly with gradient
- [ ] Sub-header visible
- [ ] Job cards have hover effects
- [ ] Match scores display with gradient background
- [ ] Tags (benefits/skills) display correctly
- [ ] Color scheme is consistent
- [ ] Buttons are properly styled
- [ ] Icons display correctly (emojis)

#### Responsive Behavior
- [ ] Resize browser window
- [ ] Layout adjusts appropriately
- [ ] Columns stack on narrow screens
- [ ] Sidebar toggleable on mobile
- [ ] All text readable at different sizes

#### Tab Navigation
- [ ] Can switch between tabs freely
- [ ] Tab state persists during session
- [ ] Content changes appropriately
- [ ] No flickering or loading issues

### 8. Performance

#### Loading Times
- [ ] Job fetching completes in reasonable time (<60s)
- [ ] Embedding generation shows progress
- [ ] Semantic search is responsive (<10s)
- [ ] Resume generation completes quickly (<30s)
- [ ] No UI freezing or lag

#### Memory Usage
- [ ] App runs smoothly with multiple searches
- [ ] Can fetch jobs multiple times without issues
- [ ] Can generate multiple resumes without degradation
- [ ] No memory warnings in browser/terminal

## 🐛 Common Issues to Check

### API Configuration
- [ ] Azure OpenAI endpoint has correct format (ends with /)
- [ ] Deployment names match actual deployments
- [ ] API keys have no extra spaces or quotes
- [ ] RapidAPI subscription is not expired

### Data Validation
- [ ] Profile saves with special characters
- [ ] Job descriptions with long text display properly
- [ ] Skills with commas parse correctly
- [ ] URLs are clickable and valid

### Edge Cases
- [ ] What happens with 0 search results?
- [ ] What if job has no skills/benefits?
- [ ] What if job URL is missing?
- [ ] Can handle very long resumes?

## 📝 Test Data Suggestions

### Sample Profile
```
Name: John Doe
Email: john.doe@email.com
Phone: +1-234-567-8900
Location: New York, NY
LinkedIn: linkedin.com/in/johndoe
Portfolio: johndoe.dev

Summary: Experienced software engineer with 5+ years in full-stack development, 
specializing in Python, React, and cloud technologies.

Experience: 
- Senior Software Engineer at Tech Corp (2021-Present)
  * Led development of microservices architecture
  * Improved application performance by 40%
  * Mentored 3 junior developers
- Software Engineer at StartupXYZ (2019-2021)
  * Built RESTful APIs using Django
  * Implemented CI/CD pipelines
  * Collaborated with design team on UX improvements

Education: 
- B.S. in Computer Science, State University (2019)
- Minor in Mathematics

Skills: 
Python, JavaScript, React, Django, Flask, PostgreSQL, MongoDB, 
AWS, Docker, Kubernetes, Git, Agile, Machine Learning, REST APIs

Certifications: 
- AWS Certified Solutions Architect (2022)
- Google Cloud Professional (2021)
```

### Sample Search Queries
1. "Python developer with cloud experience and microservices architecture knowledge"
2. "Frontend engineer skilled in React and modern JavaScript frameworks"
3. "Data scientist with machine learning and Python expertise"
4. "Full-stack developer comfortable with both frontend and backend technologies"

## ✨ Success Criteria

All features are working if:
- ✅ Profile can be created and saved
- ✅ Jobs can be fetched from Indeed
- ✅ Semantic search returns relevant results
- ✅ Resumes are generated with tailored content
- ✅ Resumes can be downloaded
- ✅ Navigation flows smoothly
- ✅ No critical errors occur
- ✅ UI is responsive and professional

## 📊 Test Results Template

Date: ___________
Tester: ___________

| Feature | Status | Notes |
|---------|--------|-------|
| Profile Management | ✅/❌ | |
| Job Fetching | ✅/❌ | |
| Semantic Search | ✅/❌ | |
| Resume Generation | ✅/❌ | |
| Download/Copy | ✅/❌ | |
| Navigation | ✅/❌ | |
| Error Handling | ✅/❌ | |
| UI/UX | ✅/❌ | |

Overall Result: ✅ PASS / ❌ FAIL

Comments:
___________________________________________
___________________________________________
___________________________________________

---

## 🎯 Next Steps After Testing

If all tests pass:
1. ✅ Application is ready for use
2. ✅ Can deploy to production
3. ✅ Share with users

If issues found:
1. Document specific errors
2. Check relevant sections in code
3. Verify API configurations
4. Review error messages
5. Consult SETUP_GUIDE.md
