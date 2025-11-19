# Quick Setup Guide

This guide will help you get the Semantic Job Search & Resume Generator up and running quickly.

## 🚦 Quick Start (5 minutes)

### 1. Install Dependencies
```bash
pip install streamlit requests numpy scikit-learn
```

### 2. Set Up API Keys

Create a file at `.streamlit/secrets.toml` with your API credentials:

```toml
AZURE_OPENAI_API_KEY = "your-key-here"
AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/"
RAPIDAPI_KEY = "your-rapidapi-key"
```

**Where to get API keys:**

#### Azure OpenAI (Required for AI features)
1. Go to [Azure Portal](https://portal.azure.com)
2. Create an Azure OpenAI resource
3. Deploy these models:
   - `text-embedding-3-small` (for semantic search)
   - `gpt-4o-mini` or `gpt-4` (for resume generation)
4. Copy the API key and endpoint from "Keys and Endpoint" section

**Note**: If your deployment names are different, update them in `app.py`:
- Line ~81: `self.deployment = "text-embedding-3-small"`
- Line ~257: `self.deployment = "gpt-4o-mini"`

#### RapidAPI (Required for job search)
1. Sign up at [RapidAPI](https://rapidapi.com)
2. Subscribe to [Indeed Scraper API](https://rapidapi.com/indeed-scraper-api/api/indeed-scraper-api)
3. Copy your RapidAPI key from the API dashboard

### 3. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📱 Using the Application

### First Time Setup

1. **Create Your Profile**
   - Click on the "My Profile" tab
   - Fill in all sections:
     - Personal info (name, email, phone)
     - Professional summary
     - Work experience
     - Education
     - Skills
     - Certifications
   - Click "Save Profile"

2. **Search for Jobs**
   - Switch to "Job Search" tab
   - Enter keywords (e.g., "Python developer")
   - Select location and filters
   - Click "Fetch Jobs"

3. **Generate Resume**
   - Click "📄 Resume" button on any job
   - Review your profile
   - Click "Generate Tailored Resume"
   - Edit if needed
   - Download or copy to clipboard
   - Click "Apply to Job" to visit the posting

## 🎯 Features Overview

### 🔍 Semantic Job Search
- Fetches real job postings from Indeed
- AI-powered matching based on meaning, not just keywords
- Shows match percentage for each job

### 📄 AI Resume Generation
- Creates custom resume for each job
- Highlights relevant experience
- Optimizes keywords for ATS systems
- Fully editable before download

### 💾 Profile Management
- Save your information once
- Reuse for all applications
- Update anytime

## 🔧 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "API Error" messages
- Check your API keys in `.streamlit/secrets.toml`
- Verify Azure OpenAI deployments are active
- Check RapidAPI subscription is active

### No jobs found
- Try different keywords
- Change location
- Increase max results
- Check internet connection

### Resume generation fails
- Verify Azure OpenAI text generation model is deployed
- Check API key has generation permissions
- Ensure profile is complete

### Low match scores
- Lower the minimum score slider
- Use more detailed search queries
- Try broader keywords

## 💡 Tips for Best Results

### Profile Tips
- Write detailed work experience (3-5 bullets per job)
- List 10-15 relevant skills
- Include quantifiable achievements
- Update education with relevant coursework

### Job Search Tips
- Use specific job titles ("Frontend Developer" vs "Developer")
- Include key technologies you want to work with
- Try different locations for more results
- Use semantic search to find non-obvious matches

### Resume Generation Tips
- Keep your profile current
- Review and edit generated resumes before sending
- Customize further for dream jobs
- Save different versions for different job types

## 🆘 Common Questions

**Q: How much do the APIs cost?**
- Azure OpenAI: Pay-per-use, ~$0.0001 per search, ~$0.02 per resume
- RapidAPI: Free tier available, check their pricing

**Q: Can I use without Azure OpenAI?**
- No, the core AI features require Azure OpenAI
- You could modify to use other LLM APIs

**Q: Is my data secure?**
- All data stored locally in your browser session
- No data is saved to external servers except API calls
- API keys are stored locally

**Q: Can I export my profile?**
- Currently stored in session state
- You can copy the profile text manually
- Future version may add export feature

**Q: What countries are supported?**
- HK, US, UK, SG, AU, CA for job search
- Resume generation works for any location

## 📚 Next Steps

1. ✅ Complete your profile thoroughly
2. ✅ Try different search queries
3. ✅ Generate resumes for multiple jobs
4. ✅ Compare different resume versions
5. ✅ Apply to your dream jobs!

## 🤝 Need Help?

If you encounter issues:
1. Check this guide first
2. Verify API keys are correct
3. Check the error message details
4. Restart the Streamlit app
5. Open an issue on GitHub

---

Happy job hunting! 🎉
