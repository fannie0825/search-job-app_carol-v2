# 📝 How to Add API Keys on macOS

Step-by-step guide for macOS users.

## 🎯 Quick Steps (macOS)

### Step 1: Open Terminal

Press `Cmd + Space` and type "Terminal", then press Enter.

### Step 2: Navigate to Your Project

```bash
cd /workspace
```

Or if your project is elsewhere:
```bash
cd ~/path/to/your/project
```

### Step 3: Create .env File

**Option A: Copy from example (Easiest)**
```bash
cp .env.example .env
```

**Option B: Create new file**
```bash
touch .env
```

### Step 4: Open .env File in Text Editor

**Option A: Using VS Code (if installed)**
```bash
code .env
```

**Option B: Using nano (built-in editor)**
```bash
nano .env
```
- Edit the file
- Press `Ctrl + O` to save
- Press `Enter` to confirm
- Press `Ctrl + X` to exit

**Option C: Using TextEdit (macOS default)**
```bash
open -a TextEdit .env
```

**Option D: Using Finder**
```bash
open .
```
Then find `.env` file and double-click it (if hidden, press `Cmd + Shift + .` to show hidden files)

### Step 5: Add Your API Keys

Copy from your Streamlit `secrets.toml` and paste into `.env`:

**Your Streamlit secrets.toml:**
```toml
AZURE_OPENAI_API_KEY = "abc123xyz789..."
AZURE_OPENAI_ENDPOINT = "https://careerlens.openai.azure.com"
RAPIDAPI_KEY = "def456uvw012..."
```

**Your React .env file:**
```env
# Backend API
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false

# Azure OpenAI (copy from Streamlit, remove quotes, add REACT_APP_ prefix)
REACT_APP_AZURE_OPENAI_API_KEY=abc123xyz789...
REACT_APP_AZURE_OPENAI_ENDPOINT=https://careerlens.openai.azure.com

# RapidAPI (copy from Streamlit, remove quotes, add REACT_APP_ prefix)
REACT_APP_RAPIDAPI_KEY=def456uvw012...
```

**Important for macOS:**
- ❌ NO quotes around values
- ❌ NO spaces around `=`
- ✅ Format: `KEY=value`
- ✅ Keep `REACT_APP_` prefix

### Step 6: Save the File

**In TextEdit:**
- Press `Cmd + S` to save

**In nano:**
- Press `Ctrl + O` (save)
- Press `Enter` (confirm)
- Press `Ctrl + X` (exit)

**In VS Code:**
- Press `Cmd + S` to save

### Step 7: Restart React App

In Terminal:
```bash
# If app is running, stop it with Ctrl + C
# Then restart:
npm start
```

## 📋 Complete Example for macOS

Here's a complete `.env` file you can copy:

```env
# ============================================
# CareerLens API Configuration
# ============================================

# Backend API URL
REACT_APP_API_URL=http://localhost:8000/api

# Use Mock API? (false = use real APIs)
REACT_APP_USE_MOCK_API=false

# ============================================
# API Keys (from Streamlit secrets.toml)
# ============================================

# Azure OpenAI API Key
REACT_APP_AZURE_OPENAI_API_KEY=your-actual-key-here-no-quotes

# Azure OpenAI Endpoint
REACT_APP_AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com

# RapidAPI Key
REACT_APP_RAPIDAPI_KEY=your-actual-key-here-no-quotes

# Backend API Key (if needed)
REACT_APP_BACKEND_API_KEY=your-backend-key-here
```

## 🖥️ Using Finder (GUI Method)

### Step 1: Show Hidden Files
1. Open Finder
2. Press `Cmd + Shift + .` (period) to show hidden files
3. Navigate to your project folder

### Step 2: Find .env.example
- Look for `.env.example` file
- Right-click → Duplicate
- Rename the copy to `.env` (remove `.example`)

### Step 3: Edit .env
- Right-click `.env` → Open With → TextEdit
- Edit and add your keys
- Press `Cmd + S` to save

## ✅ Verify It Works

In Terminal:
```bash
# Check your configuration
npm run check-env
```

You should see:
```
✅ REACT_APP_AZURE_OPENAI_API_KEY = abc123...xyz567
✅ REACT_APP_AZURE_OPENAI_ENDPOINT = https://...
✅ REACT_APP_RAPIDAPI_KEY = xyz789...vwx234
```

## 🔍 macOS-Specific Tips

### Finding Your Project Folder
```bash
# In Terminal, find where you are:
pwd

# Or open Finder to current folder:
open .
```

### If .env File is Hidden
```bash
# Show hidden files in Finder
defaults write com.apple.finder AppleShowAllFiles TRUE
killall Finder

# Hide again later:
defaults write com.apple.finder AppleShowAllFiles FALSE
killall Finder
```

### Using VS Code (Recommended)
```bash
# Install VS Code if not installed:
# Download from: https://code.visualstudio.com

# Open project in VS Code:
code .

# Then open .env file:
# File → Open File → .env
```

## ⚠️ Common macOS Mistakes

### ❌ Wrong:
```env
REACT_APP_AZURE_OPENAI_API_KEY = "abc123"  # Has quotes and spaces
REACT_APP_AZURE_OPENAI_API_KEY="abc123"   # Has quotes
REACT_APP_AZURE_OPENAI_API_KEY = abc123   # Has spaces
```

### ✅ Correct:
```env
REACT_APP_AZURE_OPENAI_API_KEY=abc123      # Perfect!
```

## 🚀 Quick Command Reference

```bash
# Navigate to project
cd /workspace

# Create .env from example
cp .env.example .env

# Open in VS Code
code .env

# Open in TextEdit
open -a TextEdit .env

# Open in nano (terminal editor)
nano .env

# Check configuration
npm run check-env

# Start React app
npm start
```

## 📍 File Location on macOS

Your `.env` file should be here:
```
/workspace/
├── .env              ← Your API keys (hidden file)
├── .env.example      ← Template (visible)
├── package.json
└── ...
```

To see hidden files in Terminal:
```bash
ls -la
```

## 🎯 Complete Workflow (Copy-Paste Ready)

```bash
# 1. Navigate to project
cd /workspace

# 2. Create .env file
cp .env.example .env

# 3. Open in editor (choose one):
code .env              # VS Code
# OR
open -a TextEdit .env  # TextEdit
# OR
nano .env              # Terminal editor

# 4. Add your keys (see example above)

# 5. Save and close editor

# 6. Verify
npm run check-env

# 7. Start app
npm start
```

## 🔧 Troubleshooting on macOS

### Problem: Can't see .env file in Finder
**Solution:**
```bash
# Show hidden files
defaults write com.apple.finder AppleShowAllFiles TRUE
killall Finder
```

### Problem: TextEdit adds formatting
**Solution:** Use VS Code or nano instead, or in TextEdit: Format → Make Plain Text

### Problem: Permission denied
**Solution:**
```bash
chmod 644 .env
```

### Problem: Changes not working
**Solution:** Make sure you restarted the React app after editing `.env`

---

**That's it!** Your API keys are now configured on macOS. 🎉
