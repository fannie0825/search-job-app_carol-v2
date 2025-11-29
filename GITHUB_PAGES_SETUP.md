# 🚀 GitHub Pages Deployment Setup

## Step-by-Step Instructions

### Step 1: Enable GitHub Pages

1. Go to your GitHub repository: `https://github.com/fannie0825/search-job-app`
2. Click on **Settings** (top menu)
3. Scroll down to **Pages** (left sidebar)
4. Under **Source**, select: **GitHub Actions**
5. Save/Leave it as is (the workflow will handle deployment)

### Step 2: Push the Deployment Workflow

The workflow file is already created at `.github/workflows/deploy.yml`. You need to commit and push it:

```bash
git add .github/workflows/deploy.yml
git add vite.config.js
git commit -m "Setup GitHub Pages deployment"
git push origin main
```

### Step 3: Trigger the Deployment

After pushing, the workflow will automatically:
1. Build your React app
2. Deploy it to GitHub Pages
3. Make it available at: `https://fannie0825.github.io/search-job-app/`

### Step 4: Check Deployment Status

1. Go to your repository on GitHub
2. Click on the **Actions** tab
3. You'll see "Deploy to GitHub Pages" workflow running
4. Wait for it to complete (usually 2-3 minutes)
5. Once it shows a green checkmark ✅, your site is live!

### Step 5: Access Your Live Site

Your app will be available at:
**https://fannie0825.github.io/search-job-app/**

---

## Automatic Deployments

Every time you push to the `main` branch, the workflow will:
- ✅ Automatically rebuild the app
- ✅ Automatically redeploy to GitHub Pages
- ✅ Update your live site

**No manual steps needed after the first setup!**

---

## Environment Variables (Optional)

If you need to set environment variables (like API URLs):

1. Go to repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add secrets:
   - `REACT_APP_API_URL` (if you have a backend)
   - `REACT_APP_USE_MOCK_API` (set to `true` or `false`)

---

## Troubleshooting

### Workflow Fails
- Check the **Actions** tab for error messages
- Common issues:
  - Missing dependencies → Check `package.json`
  - Build errors → Check build logs
  - Permission issues → Ensure Pages is enabled

### Site Shows 404
- Wait a few minutes after deployment
- Clear browser cache
- Check the base path in `vite.config.js` matches your repo name

### Blank Page After Deployment
- Open browser console (F12) to check for errors
- Verify all assets are loading
- Check if environment variables are set correctly

---

## Current Status

✅ **Workflow Created:** `.github/workflows/deploy.yml`
✅ **Vite Config Updated:** Base path configured for GitHub Pages
✅ **Ready to Deploy:** Just push to main branch!

---

## Next Steps

1. **Enable GitHub Pages** (Settings → Pages → GitHub Actions)
2. **Push the workflow** (git add, commit, push)
3. **Wait for deployment** (check Actions tab)
4. **Visit your site** (https://fannie0825.github.io/search-job-app/)

**That's it! Your app will be live on GitHub Pages! 🎉**
