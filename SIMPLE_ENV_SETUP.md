# 🎯 Simple Environment Setup (No Terminal Commands)

Easy ways to set up your API keys without using terminal commands.

## Method 1: Using Finder + TextEdit (Easiest for macOS)

### Step 1: Open Finder
1. Click Finder icon in dock
2. Press `Cmd + Shift + G` (Go to Folder)
3. Type: `/Users/tiffanyhowing/job-search-app`
4. Press Enter

### Step 2: Find .env.example
1. Look for file named `.env.example`
2. If you don't see it, press `Cmd + Shift + .` (period) to show hidden files
3. Right-click `.env.example` → Duplicate
4. Rename the copy to `.env` (remove `.example`)

### Step 3: Open .env in TextEdit
1. Right-click `.env` file
2. Open With → TextEdit
3. Edit the file

### Step 4: Add Your API Keys

**From your Streamlit secrets.toml, copy these:**
```
AZURE_OPENAI_API_KEY = "your-key-here"
AZURE_OPENAI_ENDPOINT = "https://your-endpoint.openai.azure.com"
RAPIDAPI_KEY = "your-key-here"
```

**Paste into .env like this (NO quotes, add REACT_APP_ prefix):**
```
REACT_APP_AZURE_OPENAI_API_KEY=your-key-here
REACT_APP_AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com
REACT_APP_RAPIDAPI_KEY=your-key-here
```

### Step 5: Save
- Press `Cmd + S` to save
- Close TextEdit

## Method 2: Using VS Code (If Installed)

### Step 1: Open VS Code
1. Open VS Code
2. File → Open Folder
3. Navigate to: `/Users/tiffanyhowing/job-search-app`
4. Click Open

### Step 2: Create .env File
1. In VS Code, look for `.env.example` in the file list
2. Right-click → Copy
3. Right-click in same folder → Paste
4. Rename the copy to `.env`

### Step 3: Edit .env
1. Click on `.env` file to open it
2. Replace placeholder values with your actual keys
3. Press `Cmd + S` to save

## Method 3: Manual File Creation

### Step 1: Create New File
1. Open Finder
2. Go to `/Users/tiffanyhowing/job-search-app`
3. Right-click in empty space → New Document → Text Document
4. Name it exactly: `.env` (with the dot at the beginning)

### Step 2: Copy This Template

Open the new `.env` file and paste this:

```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=paste-your-key-here
REACT_APP_AZURE_OPENAI_ENDPOINT=paste-your-endpoint-here
REACT_APP_RAPIDAPI_KEY=paste-your-key-here
```

### Step 3: Replace Placeholders
- Replace `paste-your-key-here` with your actual keys from Streamlit
- No quotes needed
- Save the file

## Method 4: Using Any Text Editor

### Step 1: Find Your Project
1. Open Finder
2. Navigate to `/Users/tiffanyhowing/job-search-app`
3. Press `Cmd + Shift + .` to show hidden files

### Step 2: Open .env.example
1. Find `.env.example`
2. Double-click to open (opens in default text editor)
3. Select All (`Cmd + A`)
4. Copy (`Cmd + C`)

### Step 3: Create .env
1. File → New (`Cmd + N`)
2. Paste (`Cmd + V`)
3. Replace placeholder values
4. Save As → Name it `.env` → Save in same folder

## 📋 Complete .env File Template

Copy this entire block and replace the values:

```
# Backend API
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false

# Azure OpenAI (from Streamlit secrets.toml)
# Copy AZURE_OPENAI_API_KEY value, remove quotes, add REACT_APP_ prefix
REACT_APP_AZURE_OPENAI_API_KEY=your-actual-key-no-quotes

# Copy AZURE_OPENAI_ENDPOINT value, remove quotes, add REACT_APP_ prefix  
REACT_APP_AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com

# RapidAPI (from Streamlit secrets.toml)
# Copy RAPIDAPI_KEY value, remove quotes, add REACT_APP_ prefix
REACT_APP_RAPIDAPI_KEY=your-actual-key-no-quotes
```

## ✅ Verification (Without Terminal)

### Check if .env File Exists:
1. Open Finder
2. Go to `/Users/tiffanyhowing/job-search-app`
3. Press `Cmd + Shift + .` to show hidden files
4. Look for `.env` file
5. If you see it, double-click to verify it has your keys

### Visual Checklist:
- [ ] `.env` file exists in project folder
- [ ] File contains `REACT_APP_AZURE_OPENAI_API_KEY=...`
- [ ] File contains `REACT_APP_AZURE_OPENAI_ENDPOINT=...`
- [ ] File contains `REACT_APP_RAPIDAPI_KEY=...`
- [ ] No quotes around values
- [ ] File is saved

## 🎨 Step-by-Step Visual Guide

### Using Finder + TextEdit:

1. **Open Finder**
   - Click Finder icon

2. **Go to Project Folder**
   - Press `Cmd + Shift + G`
   - Type: `/Users/tiffanyhowing/job-search-app`
   - Press Enter

3. **Show Hidden Files**
   - Press `Cmd + Shift + .` (period key)
   - Now you'll see files starting with `.`

4. **Find .env.example**
   - Look for file named `.env.example`
   - Right-click → Duplicate
   - Rename copy to `.env`

5. **Edit .env**
   - Double-click `.env` to open
   - Replace `your-azure-openai-api-key-here` with your actual key
   - Replace `your-rapidapi-key-here` with your actual key
   - Save (`Cmd + S`)

## 🔍 Troubleshooting

### Problem: Can't see .env.example
**Solution:** Press `Cmd + Shift + .` in Finder to show hidden files

### Problem: Can't create .env file
**Solution:** 
1. Open `.env.example` in TextEdit
2. Select All (`Cmd + A`)
3. Copy (`Cmd + C`)
4. File → New
5. Paste (`Cmd + V`)
6. Save As → Name it `.env`

### Problem: File won't save
**Solution:**
1. Make sure you're saving in the project folder
2. Make sure filename is exactly `.env` (with the dot)
3. Try saving to Desktop first, then move it to project folder

### Problem: Don't know where project folder is
**Solution:**
1. Open VS Code (if you have it)
2. File → Open Recent → Look for job-search-app
3. Or check your GitHub Desktop app for the folder location

## 💡 Pro Tip: Use VS Code

If you have VS Code installed:
1. Open VS Code
2. File → Open Folder
3. Navigate to `/Users/tiffanyhowing/job-search-app`
4. You'll see all files in the sidebar
5. Right-click `.env.example` → Copy
6. Right-click in sidebar → Paste
7. Rename to `.env`
8. Edit and save

---

**No terminal commands needed! Just use Finder and TextEdit.** 🎉
