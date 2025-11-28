# 🔍 How to Find Your job-search-app Folder on macOS

## Quick Methods to Locate Your Project

### Method 1: Using Terminal (Easiest)

**Step 1: Open Terminal**
- Press `Cmd + Space`
- Type "Terminal"
- Press Enter

**Step 2: Search for your folder**
```bash
# Search in your home directory
find ~ -name "job-search-app" -type d 2>/dev/null

# Or search everywhere (might take longer)
find / -name "job-search-app" -type d 2>/dev/null | head -5
```

**Step 3: Navigate to it**
```bash
# Once you find the path, navigate there
cd ~/path/to/job-search-app

# Common locations:
cd ~/Documents/job-search-app
# OR
cd ~/Desktop/job-search-app
# OR
cd ~/Projects/job-search-app
# OR
cd ~/job-search-app
```

### Method 2: Using Finder (GUI)

**Step 1: Open Finder**
- Click Finder icon in dock
- Or press `Cmd + Space` and type "Finder"

**Step 2: Search for folder**
- Press `Cmd + F` (or File → Find)
- Type "job-search-app" in search box
- Make sure "Kind" is set to "Folder" or "All"

**Step 3: Open the folder**
- Double-click on "job-search-app" when found
- Right-click → "New Terminal at Folder" (if available)

### Method 3: Check Common Locations

Try these common places:

```bash
# Check Desktop
ls ~/Desktop | grep job-search

# Check Documents
ls ~/Documents | grep job-search

# Check home directory
ls ~ | grep job-search

# Check Downloads (if you cloned it there)
ls ~/Downloads | grep job-search
```

### Method 4: If You Cloned from GitHub

If you cloned the repository, it's probably in:
```bash
# Check where you usually clone projects
cd ~
ls -la | grep -E "Projects|Code|Development|repos"

# Or check recent git clones
cd ~
find . -name ".git" -type d -path "*/job-search-app/.git" 2>/dev/null
```

## 🎯 Quick Command to Find It

Run this in Terminal:
```bash
# Find job-search-app folder
find ~ -maxdepth 5 -name "job-search-app" -type d 2>/dev/null
```

This will show you the full path, then:
```bash
cd /path/that/was/shown
```

## 📍 Once You Find It

**Verify you're in the right place:**
```bash
# Check you're in the right folder
pwd
# Should show: /Users/yourname/path/to/job-search-app

# Check for important files
ls -la | grep -E "package.json|\.env|components"

# See all files
ls -la
```

## 🔄 If You Can't Find It

### Option 1: Clone Fresh from GitHub
```bash
# Go to where you want the project
cd ~/Documents  # or ~/Desktop, or wherever you want it

# Clone your repository
git clone <your-github-repo-url> job-search-app

# Navigate into it
cd job-search-app
```

### Option 2: Check GitHub for the URL
1. Go to your GitHub repository
2. Click green "Code" button
3. Copy the URL
4. Use it in the clone command above

## ✅ Verify Everything is There

Once you're in the folder:
```bash
# Check you're in job-search-app
pwd

# See all files
ls -la

# Check for React components
ls components/

# Check for .env.example
ls -la .env.example

# Check git status
git status
```

## 🎯 Complete Workflow

```bash
# 1. Find your folder
find ~ -maxdepth 5 -name "job-search-app" -type d 2>/dev/null

# 2. Navigate to it (use the path from step 1)
cd ~/path/to/job-search-app

# 3. Verify you're in the right place
pwd
ls -la

# 4. Check git status
git status

# 5. Pull latest if needed
git pull origin main

# 6. Create .env file
cp .env.example .env

# 7. Open in editor
code .env
# OR
open -a TextEdit .env
```

## 💡 Pro Tip: Create an Alias

Add this to your `~/.zshrc` (or `~/.bash_profile`):
```bash
# Add to ~/.zshrc
alias jobapp='cd ~/path/to/job-search-app'
```

Then reload:
```bash
source ~/.zshrc
```

Now you can just type `jobapp` to go there!

## 🚨 Still Can't Find It?

1. **Check if it has a different name:**
   ```bash
   find ~ -type d -name "*job*" 2>/dev/null
   find ~ -type d -name "*search*" 2>/dev/null
   find ~ -type d -name "*career*" 2>/dev/null
   ```

2. **Check recent folders:**
   ```bash
   ls -lt ~/Documents | head -10
   ls -lt ~/Desktop | head -10
   ```

3. **Check if it's in a subfolder:**
   ```bash
   find ~ -type d -name "*app*" 2>/dev/null | grep -i job
   ```

---

**Once you find it, remember the path for next time!** 📍
