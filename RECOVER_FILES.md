# 🔄 File Recovery Guide

## ✅ Good News: Your Files Are Still There!

If you think files were removed after pushing to GitHub, here's how to check and recover:

## 🔍 Check What Files You Have

### 1. List All Files
```bash
# See all files including hidden ones
ls -la

# See React components
ls components/

# See services
ls services/

# See hooks
ls hooks/
```

### 2. Check Git Status
```bash
git status
```

### 3. See What's Committed
```bash
git ls-files
```

## 🔄 Recover Files from GitHub

If files are missing locally but exist on GitHub:

### Method 1: Pull from GitHub
```bash
# Get latest from GitHub
git pull origin main

# Or if on a different branch
git pull origin your-branch-name
```

### Method 2: Checkout Specific Files
```bash
# Restore a specific file from GitHub
git checkout origin/main -- path/to/file.jsx

# Example:
git checkout origin/main -- components/DashboardLayout.jsx
```

### Method 3: Reset to Last Commit
```bash
# WARNING: This discards local changes!
# Only use if you're sure

# See what would be lost
git status

# Reset to match GitHub
git reset --hard origin/main
```

## 📁 Important Files That Should Exist

### Components:
- ✅ `components/DashboardLayout.jsx`
- ✅ `components/Sidebar.jsx`
- ✅ `components/MarketPositionCards.jsx`
- ✅ `components/JobMatchTable.jsx`
- ✅ `components/Logo.jsx`
- ✅ `components/Toast.jsx`
- ✅ `components/LoadingSpinner.jsx`

### Services:
- ✅ `services/api.js`
- ✅ `services/mockApi.js`

### Hooks:
- ✅ `hooks/useToast.js`
- ✅ `hooks/useFileUpload.js`
- ✅ `hooks/useLocalStorage.js`

### Config:
- ✅ `config/api.config.js`
- ✅ `tailwind.config.js`
- ✅ `globals.css`

### Root Files:
- ✅ `App.jsx`
- ✅ `package.json`
- ✅ `.env.example`
- ✅ `.gitignore`

## 🚨 If Files Are Actually Missing

### Check Git History
```bash
# See recent commits
git log --oneline -10

# See what changed in a commit
git show <commit-hash>

# See what files were deleted
git log --diff-filter=D --summary
```

### Restore from Git History
```bash
# Find when file was deleted
git log --all --full-history -- path/to/file.jsx

# Restore from a specific commit
git checkout <commit-hash> -- path/to/file.jsx
```

### Recover from GitHub Web Interface
1. Go to your GitHub repository
2. Click on the file you need
3. Click "Raw" button
4. Copy the content
5. Create the file locally with that content

## 🔒 Important: .env File

**The `.env` file is NOT in git** (by design - it's in `.gitignore`)

If your `.env` is missing, that's normal! You need to create it:

```bash
# Create from example
cp .env.example .env

# Then edit it with your API keys
code .env
```

## ✅ Verify Everything is There

Run this check:
```bash
# Check all important files
echo "Checking files..."
[ -f "App.jsx" ] && echo "✅ App.jsx" || echo "❌ App.jsx missing"
[ -f "components/DashboardLayout.jsx" ] && echo "✅ DashboardLayout.jsx" || echo "❌ DashboardLayout.jsx missing"
[ -f "services/api.js" ] && echo "✅ api.js" || echo "❌ api.js missing"
[ -f "package.json" ] && echo "✅ package.json" || echo "❌ package.json missing"
[ -f ".env.example" ] && echo "✅ .env.example" || echo "❌ .env.example missing"
[ -f ".env" ] && echo "✅ .env (your keys)" || echo "⚠️  .env (create from .env.example)"
```

## 🎯 Quick Recovery Commands

### If you accidentally deleted files:
```bash
# Restore all files from last commit
git checkout HEAD -- .

# Or restore specific directory
git checkout HEAD -- components/
```

### If files are different from GitHub:
```bash
# See differences
git diff

# Pull latest from GitHub
git pull origin main
```

### If you want to start fresh:
```bash
# Clone again (in a new folder)
cd ..
git clone <your-repo-url> careerlens-backup
cd careerlens-backup
```

## 📞 Still Having Issues?

1. **Check what branch you're on:**
   ```bash
   git branch
   ```

2. **See all branches:**
   ```bash
   git branch -a
   ```

3. **Switch to main branch:**
   ```bash
   git checkout main
   git pull origin main
   ```

4. **List all files in repository:**
   ```bash
   git ls-files
   ```

---

**Remember:** Files in `.gitignore` (like `.env`) won't be in git - that's intentional for security!
