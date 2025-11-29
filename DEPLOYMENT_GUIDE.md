# 🚀 Deployment Guide

## Understanding the Difference

### GitHub vs. Deployed App

- **GitHub** = Source code repository (where your code lives)
- **Localhost** = Development server (only you can see it)
- **Deployed App** = Public website (everyone can access it)

**Your code on GitHub is NOT automatically a live website!** You need to deploy it.

---

## Deployment Options

### Option 1: GitHub Pages (Free, Easy)

**Pros:**
- Free
- Automatic deployment on push
- Works with your existing GitHub repo

**Cons:**
- Public repository required (or GitHub Pro)
- Limited to static sites
- URL: `https://yourusername.github.io/careerlens/`

**Setup:**
1. Go to your GitHub repo → Settings → Pages
2. Enable GitHub Pages
3. The workflow I created will auto-deploy on push to `main`

### Option 2: Vercel (Recommended - Free, Best for React)

**Pros:**
- Free tier
- Automatic deployments
- Custom domain support
- Better performance
- URL: `https://careerlens.vercel.app`

**Setup:**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

Or connect your GitHub repo at: https://vercel.com

### Option 3: Netlify (Free, Easy)

**Pros:**
- Free tier
- Easy setup
- URL: `https://careerlens.netlify.app`

**Setup:**
```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod
```

Or connect your GitHub repo at: https://app.netlify.com

---

## Quick Deploy to Vercel (Recommended)

### Method 1: Via Website (Easiest)

1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "New Project"
4. Import your GitHub repository
5. Vercel auto-detects Vite/React
6. Add environment variables if needed:
   - `REACT_APP_API_URL` (your backend URL)
   - `REACT_APP_USE_MOCK_API` (set to `true` for testing)
7. Click "Deploy"
8. Done! Your app is live in ~2 minutes

### Method 2: Via CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# For production
vercel --prod
```

---

## Environment Variables

When deploying, you'll need to set environment variables:

### For Vercel/Netlify:
1. Go to Project Settings → Environment Variables
2. Add:
   - `REACT_APP_API_URL` = Your backend API URL
   - `REACT_APP_USE_MOCK_API` = `true` (for testing) or `false` (for production)

### For GitHub Pages:
Set as GitHub Secrets:
1. Repo → Settings → Secrets and variables → Actions
2. Add secrets:
   - `REACT_APP_API_URL`
   - `REACT_APP_USE_MOCK_API`

---

## Current Status

✅ **Code is on GitHub** (source code)
❌ **App is NOT deployed yet** (not publicly accessible)
✅ **Ready to deploy** (build works, code is fixed)

---

## Next Steps

1. **Choose a deployment platform** (Vercel recommended)
2. **Deploy the app** (follow steps above)
3. **Set environment variables** (if using real backend)
4. **Test the deployed app** (visit the URL)

---

## After Deployment

Your app will be accessible at:
- **Vercel:** `https://your-app-name.vercel.app`
- **Netlify:** `https://your-app-name.netlify.app`
- **GitHub Pages:** `https://yourusername.github.io/careerlens/`

**No more localhost!** The app will be live and accessible to everyone.

---

## Troubleshooting

### "Blank page after deployment"
- Check browser console for errors
- Verify environment variables are set
- Check build logs in deployment platform

### "API calls failing"
- Update `REACT_APP_API_URL` to your production backend URL
- Or set `REACT_APP_USE_MOCK_API=true` to use mock data

### "404 errors"
- Check base path in `vite.config.js`
- For GitHub Pages, ensure base is set to `/repo-name/`

---

## Summary

**Before:** Code on GitHub → Only you can see it (localhost)
**After:** Code on GitHub → Deployed to Vercel/Netlify → Everyone can see it!

**The deployment makes your GitHub code into a live website!**
