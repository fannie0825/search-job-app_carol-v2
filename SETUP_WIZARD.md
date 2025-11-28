# 🧙 Setup Wizard - Step by Step

Follow these steps in order - no terminal commands needed!

## Step 1: Find Your Project Folder

1. Open **Finder**
2. Press `Cmd + Shift + G` (Go to Folder)
3. Type: `/Users/tiffanyhowing/job-search-app`
4. Press Enter

## Step 2: Show Hidden Files

1. In Finder, press `Cmd + Shift + .` (period key)
2. Now you'll see files starting with `.` (like `.env.example`)

## Step 3: Create .env File

**Option A: Copy from .env.example**
1. Find `.env.example` file
2. Right-click → Duplicate
3. Rename the copy to `.env` (remove `.example`)

**Option B: Create New File**
1. Right-click in empty space → New Document → Text Document
2. Name it exactly: `.env` (with the dot)
3. If it asks for extension, just use `.env`

## Step 4: Open .env File

1. Double-click `.env` file
2. It should open in TextEdit

## Step 5: Get Your Keys from Streamlit

1. Open your Streamlit project
2. Find `.streamlit/secrets.toml` file
3. Open it and copy these values:
   - `AZURE_OPENAI_API_KEY`
   - `AZURE_OPENAI_ENDPOINT`
   - `RAPIDAPI_KEY`

## Step 6: Fill in .env File

In your `.env` file, write this (replace with your actual keys):

```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=paste-your-key-here-no-quotes
REACT_APP_AZURE_OPENAI_ENDPOINT=paste-your-endpoint-here-no-quotes
REACT_APP_RAPIDAPI_KEY=paste-your-key-here-no-quotes
```

**Important:**
- Remove quotes from Streamlit values
- Add `REACT_APP_` prefix to each key name
- No spaces around `=` sign

## Step 7: Save

1. Press `Cmd + S` to save
2. Close TextEdit

## Step 8: Verify

1. Go back to Finder
2. Make sure `.env` file is there
3. Double-click to open and verify your keys are saved

## Step 9: Start Your App

**If you use VS Code:**
1. Open VS Code
2. File → Open Folder → `/Users/tiffanyhowing/job-search-app`
3. Open Terminal in VS Code (`Ctrl + ~`)
4. Type: `npm start`

**If you use other editor:**
- Open Terminal app
- Type: `cd /Users/tiffanyhowing/job-search-app`
- Type: `npm start`

---

**That's it! Your environment is configured.** ✅
