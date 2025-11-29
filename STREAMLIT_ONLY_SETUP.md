# 🎯 Streamlit App Only - Complete Setup & Deployment Guide

## Why There's a React App in the Repository

The React app (`App.jsx`, `package.json`, etc.) appears to be:
- A separate frontend project that was added
- Or an alternative UI approach
- **You don't need it** - we'll focus only on Streamlit

**You can ignore all React-related files.** We'll only use `app.py` (Streamlit).

---

## 🚀 Step 1: Test Streamlit App Locally

### Install Dependencies

```bash
cd ~/Desktop/job-search-app

# Install Python dependencies
pip install -r requirements.txt
```

**If you get errors:**
```bash
# Try with pip3
pip3 install -r requirements.txt

# Or use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# OR: venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### Set Up API Keys

Create the secrets file:

```bash
# Copy the example
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit it
nano .streamlit/secrets.toml
```

**Add your API keys:**

```toml
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = "your-actual-azure-key-here"
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com"

# RapidAPI Configuration
RAPIDAPI_KEY = "your-actual-rapidapi-key-here"
```

**Save:** `Ctrl+O`, `Enter`, `Ctrl+X`

### Run the Streamlit App

```bash
streamlit run app.py
```

**Expected:**
- Terminal shows: "You can now view your Streamlit app in your browser"
- Browser opens automatically at `http://localhost:8501`
- You see the CareerLens dashboard

**If it works:** ✅ Great! Ready for deployment.

**If you see errors:** Share them and we'll fix them.

---

## 🚀 Step 2: Prepare for Streamlit Cloud Deployment

### Check Your Files

Make sure these files exist:

```bash
# Check main app file
ls -la app.py

# Check requirements
ls -la requirements.txt

# Check secrets example (you'll add real secrets in Streamlit Cloud)
ls -la .streamlit/secrets.toml.example
```

### Verify .gitignore

Make sure `.streamlit/secrets.toml` is in `.gitignore` (so you don't commit your keys):

```bash
cat .gitignore | grep secrets.toml
```

**Should show:** `.streamlit/secrets.toml`

If not, add it:
```bash
echo ".streamlit/secrets.toml" >> .gitignore
```

---

## 🚀 Step 3: Deploy to Streamlit Cloud

### Prerequisites

1. ✅ GitHub account
2. ✅ Your code pushed to GitHub
3. ✅ Streamlit Cloud account (free at share.streamlit.io)

### Deployment Steps

#### Step 3.1: Push to GitHub

```bash
# Make sure you're in the project folder
cd ~/Desktop/job-search-app

# Check git status
git status

# Add all files (except secrets.toml - it's in .gitignore)
git add .

# Commit
git commit -m "Ready for Streamlit Cloud deployment"

# Push to GitHub
git push origin main
```

**Note:** Make sure `.streamlit/secrets.toml` is NOT committed (it's in `.gitignore`).

#### Step 3.2: Deploy on Streamlit Cloud

1. **Go to:** https://share.streamlit.io
2. **Sign in** with GitHub
3. **Click:** "New app"
4. **Select:**
   - **Repository:** Your GitHub repo (`search-job-app` or similar)
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. **Click:** "Deploy!"

#### Step 3.3: Add Secrets in Streamlit Cloud

After deployment:

1. **Go to your app** on Streamlit Cloud
2. **Click:** "Settings" (⚙️ icon) or "Manage app"
3. **Go to:** "Secrets" tab
4. **Add your secrets:**

```toml
AZURE_OPENAI_API_KEY = "your-actual-azure-key"
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com"
RAPIDAPI_KEY = "your-actual-rapidapi-key"
```

5. **Save** - Your app will automatically restart with the new secrets

---

## ✅ Step 4: Verify Deployment

1. **Visit your app:** `https://your-app-name.streamlit.app`
2. **Test features:**
   - Create profile
   - Search jobs
   - Generate resume
3. **Check for errors** in the app interface

---

## 🐛 Troubleshooting

### Problem: "Module not found" when running locally

**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: "Secrets not found" error

**Solution:**
- Make sure `.streamlit/secrets.toml` exists locally
- Make sure secrets are added in Streamlit Cloud settings

### Problem: App won't deploy on Streamlit Cloud

**Solution:**
- Check that `app.py` is in the root of your repo
- Check that `requirements.txt` exists
- Check Streamlit Cloud logs for errors

### Problem: API errors in deployed app

**Solution:**
- Verify secrets are correctly set in Streamlit Cloud
- Check API keys are valid
- Check Azure OpenAI deployments are active

---

## 📋 Quick Checklist

Before deploying:

- [ ] Streamlit app runs locally (`streamlit run app.py`)
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Secrets file created locally (`.streamlit/secrets.toml`)
- [ ] Code pushed to GitHub
- [ ] `.streamlit/secrets.toml` is in `.gitignore` (not committed)
- [ ] Ready to add secrets in Streamlit Cloud

---

## 🎯 Summary

**You only need:**
1. ✅ `app.py` - Your Streamlit application
2. ✅ `requirements.txt` - Python dependencies
3. ✅ `.streamlit/secrets.toml` - API keys (local) and in Streamlit Cloud

**You can ignore:**
- ❌ All React files (`App.jsx`, `package.json`, `src/`, etc.)
- ❌ `.env` file (that's for React)
- ❌ Vite configuration

**Focus only on Streamlit!**

---

## Next Steps

1. **Test locally:** `streamlit run app.py`
2. **If it works:** Push to GitHub and deploy to Streamlit Cloud
3. **If errors:** Share them and we'll fix them

Let's start by testing the Streamlit app locally!
