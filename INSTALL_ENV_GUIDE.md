# 📦 Complete Guide: Installing .env File on Your Local Computer

This guide will walk you through setting up your `.env` file on Windows, macOS, and Linux.

## 🎯 What is a .env File?

A `.env` file stores your API keys and configuration settings locally on your computer. It's like a password file that your application reads to connect to external services.

**Important:** 
- The `.env` file is **NOT** committed to git (it's in `.gitignore`)
- Keep your `.env` file **private** - never share it publicly
- Each developer needs their own `.env` file with their own API keys

---

## 📋 Prerequisites

Before you start, make sure you have:
- ✅ Your project folder open
- ✅ Your API keys ready (Azure OpenAI, RapidAPI, etc.)
- ✅ A text editor (VS Code, Notepad, TextEdit, or any editor)

---

## 🚀 Quick Start (Choose Your Method)

### Method 1: Copy from Template (Easiest) ⭐

This is the fastest way to create your `.env` file.

#### On Windows:
1. Open File Explorer
2. Navigate to your project folder (where `package.json` is located)
3. Find the file named `.env.example` or `.env.template`
4. Right-click → **Copy**
5. Right-click in the same folder → **Paste**
6. Right-click the copied file → **Rename**
7. Change the name from `.env.example` to `.env` (remove `.example`)
8. Press Enter

#### On macOS:
1. Open Finder
2. Navigate to your project folder
3. Press `Cmd + Shift + .` (period) to show hidden files
4. Find `.env.example` or `.env.template`
5. Right-click → **Duplicate**
6. Rename the copy to `.env` (remove `.example`)

#### On Linux:
```bash
# Open terminal in your project folder
cd /path/to/your/project

# Copy the template
cp .env.example .env
```

### Method 2: Create New File Manually

If you can't find `.env.example`, create a new file:

#### On Windows:
1. Open File Explorer → Navigate to project folder
2. Right-click in empty space → **New** → **Text Document**
3. Name it exactly: `.env` (with the dot at the beginning)
4. If Windows warns about changing extension, click **Yes**

#### On macOS:
1. Open Finder → Navigate to project folder
2. Open **TextEdit** (Applications → TextEdit)
3. Create a new document (`Cmd + N`)
4. Save As (`Cmd + Shift + S`)
5. Name it: `.env`
6. Choose location: your project folder
7. Click **Save**

#### On Linux:
```bash
# Create empty .env file
touch .env

# Or open in editor
nano .env
```

---

## ✏️ Step 2: Edit the .env File

Now you need to add your API keys to the `.env` file.

### Option A: Using VS Code (Recommended)

1. Open VS Code
2. File → **Open Folder** → Select your project folder
3. Click on `.env` in the file explorer (left sidebar)
4. Edit the file (see content below)
5. Save (`Ctrl+S` on Windows/Linux, `Cmd+S` on Mac)

### Option B: Using Any Text Editor

1. Right-click `.env` file
2. **Open with** → Choose your text editor
3. Edit the file
4. Save

### What to Put in Your .env File

Copy this template and replace the placeholder values with your actual API keys:

```env
# ============================================
# CareerLens API Configuration
# ============================================

# Backend API URL
REACT_APP_API_URL=http://localhost:8000/api

# Use Mock API? (set to false to use real APIs)
REACT_APP_USE_MOCK_API=false

# ============================================
# API Keys - Replace with your actual keys
# ============================================

# Azure OpenAI API Key
# Get this from: https://portal.azure.com → Your OpenAI Resource → Keys and Endpoint
REACT_APP_AZURE_OPENAI_API_KEY=your-azure-openai-api-key-here

# Azure OpenAI Endpoint
# Format: https://your-resource-name.openai.azure.com
REACT_APP_AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com

# RapidAPI Key
# Get this from: https://rapidapi.com → Dashboard → Your API Key
REACT_APP_RAPIDAPI_KEY=your-rapidapi-key-here

# Backend API Key (if your backend requires authentication)
REACT_APP_BACKEND_API_KEY=your-backend-api-key-here
```

### ⚠️ Important Formatting Rules

**✅ DO:**
- Use format: `KEY=value` (no spaces around `=`)
- No quotes around values
- One key per line
- Keep the `REACT_APP_` prefix

**❌ DON'T:**
- ❌ `REACT_APP_KEY = "value"` (no spaces, no quotes)
- ❌ `REACT_APP_KEY="value"` (no quotes)
- ❌ `REACT_APP_KEY= value` (no spaces)

### Example of Correct Format:

```env
REACT_APP_AZURE_OPENAI_API_KEY=abc123def456ghi789jkl012mno345pqr678
REACT_APP_AZURE_OPENAI_ENDPOINT=https://careerlens.openai.azure.com
REACT_APP_RAPIDAPI_KEY=xyz789abc123def456ghi789jkl012mno345pqr678
```

---

## 🔑 Where to Get Your API Keys

### Azure OpenAI API Key

1. Go to [Azure Portal](https://portal.azure.com)
2. Sign in with your Azure account
3. Navigate to your **Azure OpenAI** resource
4. Click **Keys and Endpoint** in the left menu
5. Copy **KEY 1** or **KEY 2**
6. Copy the **Endpoint** URL
7. Paste them into your `.env` file

### RapidAPI Key

1. Go to [RapidAPI](https://rapidapi.com)
2. Sign in or create an account
3. Click your profile icon → **Dashboard**
4. Find **Your API Key** section
5. Copy the key
6. Paste it into your `.env` file

---

## ✅ Step 3: Verify Your .env File

### Check File Location

Your `.env` file should be in the **root** of your project folder, at the same level as `package.json`:

```
your-project/
├── .env              ← Should be here
├── .env.example      ← Template file
├── package.json
├── src/
└── components/
```

### Check File Contents

Open your `.env` file and verify:
- [ ] File exists in project root
- [ ] Contains `REACT_APP_AZURE_OPENAI_API_KEY=...` (with actual key, not placeholder)
- [ ] Contains `REACT_APP_AZURE_OPENAI_ENDPOINT=...` (with actual endpoint)
- [ ] Contains `REACT_APP_RAPIDAPI_KEY=...` (with actual key)
- [ ] No quotes around values
- [ ] No spaces around `=` signs
- [ ] All keys start with `REACT_APP_`

### Test Your Configuration

If your project has a check script, run it:

```bash
# In your project folder
npm run check-env
```

Or manually verify by starting your app:

```bash
npm start
```

If the app starts without API key errors, your `.env` file is working! 🎉

---

## 🔄 Step 4: Restart Your Application

**IMPORTANT:** After creating or editing your `.env` file, you **MUST** restart your application:

1. Stop your current app (press `Ctrl+C` in terminal)
2. Start it again:
   ```bash
   npm start
   ```

React apps only read `.env` files when they start, so changes won't take effect until you restart.

---

## 🖥️ Platform-Specific Instructions

### Windows

#### Using Command Prompt:
```cmd
cd C:\path\to\your\project
copy .env.example .env
notepad .env
```

#### Using PowerShell:
```powershell
cd C:\path\to\your\project
Copy-Item .env.example .env
notepad .env
```

#### Using File Explorer:
1. Navigate to project folder
2. Enable "Show hidden files" (View → Show → Hidden items)
3. Find `.env.example`
4. Copy and rename to `.env`
5. Open with Notepad or VS Code

### macOS

#### Using Terminal:
```bash
cd ~/path/to/your/project
cp .env.example .env
open -a TextEdit .env
# Or use VS Code:
code .env
```

#### Using Finder:
1. Open Finder
2. Press `Cmd + Shift + G` (Go to Folder)
3. Type your project path
4. Press `Cmd + Shift + .` to show hidden files
5. Find `.env.example` → Duplicate → Rename to `.env`
6. Double-click to open in TextEdit

### Linux

#### Using Terminal:
```bash
cd /path/to/your/project
cp .env.example .env
nano .env
# Or use VS Code:
code .env
# Or use vim:
vim .env
```

#### Using File Manager:
1. Open your file manager (Nautilus, Dolphin, etc.)
2. Press `Ctrl + H` to show hidden files
3. Navigate to project folder
4. Copy `.env.example` → Rename to `.env`
5. Right-click → Open with text editor

---

## 🐛 Troubleshooting

### Problem: Can't see .env.example file

**Solution:**
- **Windows:** View → Show → Hidden items
- **macOS:** Press `Cmd + Shift + .` in Finder
- **Linux:** Press `Ctrl + H` in file manager

### Problem: Can't create .env file

**Solution:**
1. Make sure you're in the project root folder
2. Check you have write permissions
3. Try creating it with a different name first (like `env.txt`), then rename to `.env`

### Problem: File won't save

**Solution:**
1. Make sure you're saving in the project folder
2. Check filename is exactly `.env` (with the dot)
3. Try saving to Desktop first, then move it to project folder

### Problem: Changes not working after editing

**Solution:**
1. **Restart your app** - React only reads `.env` on startup
2. Check for typos in variable names
3. Verify no quotes around values
4. Check no spaces around `=` signs

### Problem: "API key is undefined" error

**Solution:**
1. Verify variable names start with `REACT_APP_`
2. Check no quotes around values
3. Check no spaces around `=`
4. Make sure file is named exactly `.env` (not `.env.txt`)
5. Restart the app

### Problem: Don't know where project folder is

**Solution:**
1. If using VS Code: File → Open Recent
2. If using Git: Check where you cloned the repository
3. Search your computer for `package.json` file

---

## 📝 Quick Reference Template

Copy this entire block into your `.env` file:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=PASTE_YOUR_KEY_HERE
REACT_APP_AZURE_OPENAI_ENDPOINT=PASTE_YOUR_ENDPOINT_HERE
REACT_APP_RAPIDAPI_KEY=PASTE_YOUR_KEY_HERE
REACT_APP_BACKEND_API_KEY=PASTE_YOUR_KEY_HERE
```

---

## ✅ Final Checklist

Before you're done, make sure:

- [ ] `.env` file exists in project root folder
- [ ] File is named exactly `.env` (with the dot)
- [ ] All API keys are filled in (no placeholders)
- [ ] No quotes around values
- [ ] No spaces around `=` signs
- [ ] All keys start with `REACT_APP_`
- [ ] File is saved
- [ ] App has been restarted after creating/editing `.env`

---

## 🎉 You're Done!

Your `.env` file is now set up! Your application should be able to connect to the APIs.

**Next Steps:**
1. Start your application: `npm start`
2. Test the features that require API keys
3. If you see errors, check the Troubleshooting section above

---

## 📚 Additional Resources

- See `HOW_TO_ADD_API_KEYS.md` for more detailed API key setup
- See `ENV_FILE_FORMAT.md` for format specifications
- See `README.md` for general project information

---

**Need Help?** If you're still having issues, check:
1. Your API keys are valid and active
2. Your `.env` file format is correct
3. You've restarted your application
4. Your project dependencies are installed (`npm install`)

Happy coding! 🚀
