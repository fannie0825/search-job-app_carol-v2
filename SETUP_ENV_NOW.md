# 🚀 Quick Setup: .env File Right Now

Follow these steps to set up your `.env` file immediately:

## Step 1: Copy the Template File

Run this command in your terminal (you're already in the right folder):

```bash
cp .env.example .env
```

## Step 2: Open the .env File

You can use any text editor. Here are your options:

### Option A: Using VS Code (if installed)
```bash
code .env
```

### Option B: Using nano (built-in terminal editor)
```bash
nano .env
```
(When done editing, press `Ctrl+X`, then `Y`, then `Enter` to save)

### Option C: Using TextEdit (macOS)
```bash
open -a TextEdit .env
```

## Step 3: Add Your API Keys

Replace the placeholder values with your actual API keys:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=your-actual-key-here
REACT_APP_AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
REACT_APP_RAPIDAPI_KEY=your-actual-key-here
REACT_APP_BACKEND_API_KEY=your-backend-key-here
```

**Important:**
- ❌ NO quotes around values
- ❌ NO spaces around the `=` sign
- ✅ Format: `KEY=value`

## Step 4: Save and Verify

1. Save the file
2. Verify it exists:
   ```bash
   ls -la .env
   ```
   You should see `.env` in the list

3. Check your configuration:
   ```bash
   npm run check-env
   ```

## Step 5: Install Missing Dependencies

The project needs Vite. Run:

```bash
npm install
```

This will install Vite and other missing dependencies.

## Step 6: Start the App

```bash
npm start
```

Or use the dev command:

```bash
npm run dev
```

The app should open at `http://localhost:3000`

---

## ✅ Quick Checklist

- [ ] Copied `.env.example` to `.env`
- [ ] Opened `.env` file in editor
- [ ] Added your actual API keys (no quotes, no spaces)
- [ ] Saved the file
- [ ] Ran `npm install` to install Vite
- [ ] Ran `npm start` or `npm run dev`
- [ ] App opened in browser

---

## 🐛 Troubleshooting

### "next: command not found"
**Fixed!** The package.json has been updated to use Vite instead of Next.js.

### "vite: command not found"
Run `npm install` again to install Vite.

### "API key is undefined"
1. Make sure your `.env` file exists in the project root
2. Check variable names start with `REACT_APP_`
3. Verify no quotes around values
4. Restart the app after editing `.env`

---

**You're all set!** 🎉
