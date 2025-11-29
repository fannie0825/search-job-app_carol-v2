# 🐛 Debug: Blank Page - Step by Step

## Step 1: Check Browser Console (CRITICAL!)

**This is the most important step!**

1. **Open Developer Tools:**
   - **Mac:** `Cmd + Option + I`
   - **Windows/Linux:** `F12` or `Ctrl + Shift + I`

2. **Go to Console tab**

3. **Look for RED error messages**

4. **Copy ALL error messages** and share them with me

**Common errors you might see:**
- `Failed to resolve import` → File path issue
- `Cannot find module` → Missing file
- `Unexpected token` → Syntax error
- `ReferenceError` → Variable not defined

---

## Step 2: Check Terminal Output

Look at your terminal where `npm start` is running.

**What do you see?**
- ✅ `VITE v5.4.21 ready` → Good
- ❌ Any red errors? → Bad, share them
- ❌ "Failed to compile" → Bad, share the error

---

## Step 3: Verify File Structure

Run these commands:

```bash
cd ~/Desktop/job-search-app

# Check all key files exist
echo "=== Checking Files ==="
ls -la index.html
ls -la App.jsx
ls -la src/main.jsx
ls -la components/DashboardLayout.jsx
ls -la globals.css
```

**All should exist.** If any are missing, that's the problem.

---

## Step 4: Test with Minimal App

Let's test if React is working at all:

```bash
nano App.jsx
```

**Replace everything with this simple test:**

```javascript
import React from 'react';

function App() {
  return (
    <div style={{ 
      padding: '50px', 
      fontSize: '24px',
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#f0f0f0',
      minHeight: '100vh',
      color: '#000'
    }}>
      <h1>✅ React is Working!</h1>
      <p>If you see this message, React is loading correctly.</p>
      <p>The issue is with the DashboardLayout component or its imports.</p>
    </div>
  );
}

export default App;
```

**Save:** `Ctrl+O`, `Enter`, `Ctrl+X`

**Refresh browser** - Do you see "React is Working!"?

- ✅ **YES** → React works! The issue is with DashboardLayout
- ❌ **NO** → There's a deeper React/Vite setup issue

---

## Step 5: Check Network Tab

1. Open Developer Tools → **Network** tab
2. Refresh page (`Cmd+R` or `Ctrl+R`)
3. Look for:
   - `main.jsx` - should be status **200** (green)
   - `App.jsx` - should be status **200** (green)
   - Any **red/failed** requests?

**Share what you see in the Network tab.**

---

## Step 6: Check for Import Errors

The most common issue is a component import failing. Let's check:

```bash
# Check if all component files exist
ls -la components/

# Check the main imports
head -10 App.jsx
head -10 src/main.jsx
```

---

## Step 7: Clear Everything and Restart

Sometimes cache causes issues:

1. **Stop the server:** `Ctrl+C` in terminal

2. **Clear node_modules and reinstall:**
   ```bash
   rm -rf node_modules
   npm install
   ```

3. **Clear browser cache:**
   - Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)

4. **Start again:**
   ```bash
   npm start
   ```

---

## What I Need From You

Please share:

1. **Browser Console Errors** (screenshot or copy/paste)
2. **Terminal Output** (any errors after "VITE ready")
3. **Result of Step 4** (do you see "React is Working!"?)
4. **Network Tab** (any failed requests?)

This will help me identify the exact problem!
