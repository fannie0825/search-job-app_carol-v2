# Streamlit Cloud Deployment Guide

## Overview
This application is configured to run **exclusively on Streamlit Cloud**. All configurations have been optimized for Streamlit Cloud deployment.

## Prerequisites

1. **GitHub Repository**
   - Your code must be in a GitHub repository
   - Repository must be public (or you need Streamlit Cloud Team plan for private repos)

2. **Streamlit Cloud Account**
   - Sign up at https://share.streamlit.io
   - Connect your GitHub account

3. **API Keys**
   - Azure OpenAI API key and endpoint
   - RapidAPI key (for job scraping)

## Deployment Steps

### Step 1: Prepare Your Repository

Ensure your repository has:
- ✅ `app.py` - Main Streamlit application
- ✅ `requirements.txt` - Python dependencies
- ✅ `.streamlit/config.toml` - Streamlit configuration (optimized for Cloud)
- ✅ `.streamlit/secrets.toml.example` - Example secrets file

### Step 2: Configure Secrets in Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Select your repository and branch
4. Set main file to: `app.py`
5. Click "Advanced settings"
6. Add the following secrets:

```toml
AZURE_OPENAI_API_KEY = "your_azure_openai_key"
AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com"
RAPIDAPI_KEY = "your_rapidapi_key"
RAPIDAPI_MAX_REQUESTS_PER_MINUTE = 3
USE_LINKEDIN_ONLY = false
SKIP_INDEED_IF_QUOTA_EXCEEDED = true
```

**Optional secrets:**
```toml
LINKEDIN_API_KEY = "separate_linkedin_key"  # Only if different from RAPIDAPI_KEY
EMBEDDING_BATCH_SIZE = 20
MAX_JOBS_TO_INDEX = 50
EMBEDDING_BATCH_DELAY = 1
```

### Step 3: Deploy

1. Click "Deploy"
2. Wait for the app to build and deploy
3. Your app will be available at: `https://your-app-name.streamlit.app`

## Configuration Details

### Streamlit Config (`.streamlit/config.toml`)

The configuration is optimized for Streamlit Cloud:
- ✅ CORS enabled for Streamlit Cloud
- ✅ XSRF protection enabled
- ✅ WebSocket compression enabled
- ✅ File watcher disabled (not needed on Cloud)
- ✅ Headless mode enabled
- ✅ Production mode (developmentMode = false)
- ✅ Error-level logging only

### App Configuration (`app.py`)

The app is configured to:
- ✅ Use `st.secrets` for all API keys (Streamlit Cloud standard)
- ✅ Handle errors gracefully
- ✅ Support large file uploads (200MB max)
- ✅ Optimize for Streamlit Cloud's infrastructure

## Environment Variables

All configuration is done through Streamlit secrets, not environment variables. This is the Streamlit Cloud standard.

## File Structure

```
.
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .streamlit/
│   ├── config.toml                # Streamlit configuration (Cloud-optimized)
│   └── secrets.toml.example       # Example secrets file
└── README.md                       # Project documentation
```

## Troubleshooting

### App Won't Deploy

1. **Check requirements.txt**
   - Ensure all dependencies are listed
   - Check for version conflicts

2. **Check app.py**
   - Ensure `st.set_page_config()` is the first Streamlit command
   - Verify no syntax errors

3. **Check Secrets**
   - Ensure all required secrets are set in Streamlit Cloud
   - Verify secret names match exactly (case-sensitive)

### App Deploys But Shows Errors

1. **Check Streamlit Cloud Logs**
   - Go to your app's settings
   - Click "View logs"
   - Look for error messages

2. **Common Issues:**
   - Missing API keys → Add secrets
   - Import errors → Check requirements.txt
   - Memory issues → Optimize code or upgrade plan

### Performance Issues

1. **Rate Limiting**
   - Adjust `RAPIDAPI_MAX_REQUESTS_PER_MINUTE` in secrets
   - Consider upgrading RapidAPI plan

2. **Large File Uploads**
   - Current max: 200MB (configured in config.toml)
   - If needed, reduce or optimize file sizes

## Best Practices

1. **Secrets Management**
   - Never commit `secrets.toml` to git
   - Always use `secrets.toml.example` as template
   - Use Streamlit Cloud secrets interface

2. **Error Handling**
   - App uses `st.secrets.get()` with fallbacks
   - Errors are displayed to users gracefully
   - Logs are set to ERROR level only

3. **Performance**
   - WebSocket compression enabled
   - Batch processing for API calls
   - Rate limiting configured

4. **Security**
   - XSRF protection enabled
   - CORS properly configured
   - Secrets stored securely in Streamlit Cloud

## Monitoring

- **Streamlit Cloud Dashboard**: Monitor app status, logs, and usage
- **Logs**: View real-time logs in Streamlit Cloud interface
- **Metrics**: Track app performance and errors

## Updates

To update your app:
1. Push changes to your GitHub repository
2. Streamlit Cloud will automatically detect changes
3. App will rebuild and redeploy automatically

## Support

- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Streamlit Forum**: https://discuss.streamlit.io
- **GitHub Issues**: Report bugs in your repository

## Notes

- This app is configured **exclusively for Streamlit Cloud**
- All local development configurations have been removed
- The app assumes Streamlit Cloud environment
- React app files are present but not used for Streamlit Cloud deployment
