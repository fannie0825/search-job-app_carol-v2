# 🔌 Understanding Ports: 3000 vs 8000

## Port Explanation

Your application uses **TWO different ports**:

### Port 3000: Frontend (React/Vite App)
- **What:** Your React application (what you see in the browser)
- **Running:** `npm start` starts Vite on port 3000
- **URL:** `http://localhost:3000`
- **Status:** ✅ This is running (you see "VITE ready")

### Port 8000: Backend API
- **What:** Your backend server (API endpoints)
- **Running:** Separate server (Python/Node.js backend)
- **URL:** `http://localhost:8000/api`
- **Status:** ❓ Might not be running

---

## How They Work Together

```
Browser (Port 3000)  →  Makes API calls  →  Backend (Port 8000)
     ↑                                              ↓
     └─────────── Returns data ───────────────────┘
```

1. **Frontend (port 3000)** displays the UI
2. **Frontend** makes API calls to **Backend (port 8000)**
3. **Backend** processes requests and returns data
4. **Frontend** displays the data

---

## Your .env File is Correct!

Your `.env` file has:
```env
REACT_APP_API_URL=http://localhost:8000/api
```

**This is correct!** The frontend (port 3000) needs to know where the backend (port 8000) is.

---

## Do You Need a Backend?

### Option 1: Use Mock API (No Backend Needed)

If your `.env` has:
```env
REACT_APP_USE_MOCK_API=true
```

**You don't need a backend!** The app will use mock/sample data.

**Check your .env:**
```bash
cat .env | grep USE_MOCK_API
```

If it says `true`, you're using mock data and don't need port 8000.

---

### Option 2: Use Real Backend (Need Port 8000)

If your `.env` has:
```env
REACT_APP_USE_MOCK_API=false
```

**You need a backend server running on port 8000.**

This would typically be:
- A Python backend (like `app.py` with Streamlit or Flask)
- A Node.js backend
- Or another API server

---

## Check Your Current Setup

Run this to see your current configuration:

```bash
cd ~/Desktop/job-search-app

echo "=== Your API Configuration ==="
cat .env | grep -E "API_URL|USE_MOCK_API"
```

**What you'll see:**

**If using Mock API:**
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=true
```
✅ **No backend needed!** App works with mock data.

**If using Real API:**
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
```
❌ **Backend needed!** You need to start a server on port 8000.

---

## If You're Using Mock API

If `REACT_APP_USE_MOCK_API=true`, then:

1. ✅ **Port 3000** is all you need (frontend)
2. ✅ **Port 8000** is not needed (using mock data)
3. ✅ **Your app should work** without a backend

**The blank page issue is NOT related to port 8000!**

---

## If You Need a Backend

If `REACT_APP_USE_MOCK_API=false`, you need to:

1. **Start your backend server** on port 8000
2. **Check if you have a backend file:**
   ```bash
   ls -la app.py  # Python backend?
   ls -la server.js  # Node.js backend?
   ```

3. **Start the backend:**
   - Python: `python app.py` or `streamlit run app.py`
   - Node.js: `node server.js` or `npm run server`

---

## Summary

- **Port 3000** = Frontend (Vite/React) - ✅ Running
- **Port 8000** = Backend API - ❓ Only needed if `USE_MOCK_API=false`
- **Your .env is correct** - port 8000 is for the backend, not frontend

**The blank page issue is likely NOT about ports!** It's probably:
- A JavaScript error (check browser console)
- A component import issue
- A CSS issue

---

## Next Steps

1. **Check if you're using mock API:**
   ```bash
   cat .env | grep USE_MOCK_API
   ```

2. **If `true`:** You don't need port 8000. Focus on fixing the blank page (check browser console).

3. **If `false`:** You need to start a backend server on port 8000.

Let me know what `USE_MOCK_API` is set to, and we'll proceed!
