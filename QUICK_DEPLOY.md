# 🚀 Quick Deploy Guide

## The Key Point

**GitHub = Source Code Storage**  
**Deployed App = Live Website**

Your code on GitHub is NOT automatically a website. You need to deploy it to make it accessible to everyone.

---

## Fastest Way: Deploy to Vercel (2 minutes)

### Step 1: Go to Vercel
Visit: https://vercel.com

### Step 2: Sign in with GitHub
Click "Sign in" → Choose GitHub → Authorize

### Step 3: Import Your Repository
1. Click "Add New Project"
2. Find your `careerlens` repository
3. Click "Import"

### Step 4: Configure (Auto-detected)
Vercel will auto-detect:
- Framework: Vite
- Build Command: `npm run build`
- Output Directory: `dist`

### Step 5: Add Environment Variables (Optional)
If you have a backend API:
- `REACT_APP_API_URL` = Your API URL
- `REACT_APP_USE_MOCK_API` = `false`

For testing (no backend):
- `REACT_APP_USE_MOCK_API` = `true`

### Step 6: Deploy!
Click "Deploy" → Wait 2 minutes → Done!

**Your app is now live at:** `https://your-app-name.vercel.app`

---

## Alternative: GitHub Pages

### Step 1: Enable GitHub Pages
1. Go to your repo on GitHub
2. Settings → Pages
3. Source: "GitHub Actions"

### Step 2: Push to Main
The workflow I created will auto-deploy:
```bash
git add .
git commit -m "Setup deployment"
git push origin main
```

### Step 3: Wait for Deployment
1. Go to Actions tab
2. Wait for "Deploy to GitHub Pages" to complete
3. Your app will be at: `https://yourusername.github.io/repo-name/`

---

## What Happens After Deployment?

✅ **Before:** Code on GitHub (only you can see it via localhost)  
✅ **After:** Live website (everyone can access it via URL)

**No more localhost!** The app is now publicly accessible.

---

## Need Help?

- **Vercel Issues:** Check deployment logs in Vercel dashboard
- **GitHub Pages Issues:** Check Actions tab for errors
- **App Not Working:** Check browser console on deployed site

---

## Summary

1. **Code on GitHub** = Source code (not a website)
2. **Deploy to Vercel/Netlify** = Makes it a live website
3. **Share the URL** = Everyone can now access it!

**The deployment process converts your GitHub code into a live website!**
