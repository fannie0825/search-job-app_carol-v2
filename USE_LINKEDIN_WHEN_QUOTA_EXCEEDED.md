# Using LinkedIn When Indeed Quota is Exceeded

If you've exceeded your Indeed API quota (e.g., 25 requests/month), you can force the app to use LinkedIn instead.

## Quick Solution

Add this to your `.streamlit/secrets.toml` file:

```toml
USE_LINKEDIN_ONLY = true
```

This will **completely skip Indeed** and use LinkedIn only for all job searches.

## Automatic Fallback (Recommended)

Alternatively, you can enable automatic switching when Indeed quota is exceeded:

```toml
SKIP_INDEED_IF_QUOTA_EXCEEDED = true
```

With this setting:
- The app will **try Indeed first**
- If Indeed returns a 429 error (quota exceeded), it will **automatically switch to LinkedIn**
- Indeed will be **skipped for the rest of the session** once quota is detected as exceeded

## Configuration Options

### Option 1: Force LinkedIn Only (Immediate)

**Best for**: You know your Indeed quota is exhausted and want to skip it entirely.

```toml
USE_LINKEDIN_ONLY = true
```

**What happens**:
- Indeed is never called
- Only LinkedIn is used
- Faster (no failed Indeed attempts)

### Option 2: Automatic Fallback (Smart)

**Best for**: You want to use Indeed when available, but automatically fall back to LinkedIn.

```toml
SKIP_INDEED_IF_QUOTA_EXCEEDED = true
```

**What happens**:
- Tries Indeed first
- If 429 error detected → automatically switches to LinkedIn
- Remembers for the session (won't try Indeed again)

### Option 3: Both Enabled

You can enable both options:

```toml
USE_LINKEDIN_ONLY = true
SKIP_INDEED_IF_QUOTA_EXCEEDED = true
```

**What happens**:
- `USE_LINKEDIN_ONLY` takes precedence
- Indeed is completely skipped

## Step-by-Step Setup

1. **Open your secrets file**:
   ```bash
   nano .streamlit/secrets.toml
   ```
   Or use your preferred text editor.

2. **Add the configuration**:
   ```toml
   # Skip Indeed and use LinkedIn only
   USE_LINKEDIN_ONLY = true
   ```

3. **Save the file** and restart your Streamlit app.

4. **Verify it's working**:
   - When you search for jobs, you should see: "ℹ️ Using LinkedIn only (Indeed skipped per configuration)"
   - Jobs will come from LinkedIn only

## Verify LinkedIn API is Available

Before enabling this, make sure:

1. **You have a LinkedIn Jobs API subscription** on RapidAPI
   - Go to [RapidAPI LinkedIn Jobs API](https://rapidapi.com/hub)
   - Search for "LinkedIn Jobs API"
   - Subscribe to a plan

2. **Your RapidAPI key works for LinkedIn**:
   - The same `RAPIDAPI_KEY` usually works for both Indeed and LinkedIn
   - If not, set `LINKEDIN_API_KEY` separately

3. **Check LinkedIn quota**:
   - Make sure your LinkedIn API quota isn't also exhausted
   - Check in RapidAPI dashboard → My APIs → LinkedIn Jobs API

## Example Configuration

Here's a complete example of your `.streamlit/secrets.toml`:

```toml
# Azure OpenAI
AZURE_OPENAI_API_KEY = "your-key"
AZURE_OPENAI_ENDPOINT = "https://your-endpoint.openai.azure.com"

# RapidAPI (works for both Indeed and LinkedIn if subscribed to both)
RAPIDAPI_KEY = "your-rapidapi-key"

# Rate limiting
RAPIDAPI_MAX_REQUESTS_PER_MINUTE = 3

# Force LinkedIn only (Indeed quota exceeded)
USE_LINKEDIN_ONLY = true

# Or use automatic fallback instead:
# SKIP_INDEED_IF_QUOTA_EXCEEDED = true
```

## Troubleshooting

### "No jobs found from any source"

**Possible causes**:
1. LinkedIn API quota also exhausted
2. LinkedIn API not subscribed
3. `RAPIDAPI_KEY` doesn't have LinkedIn access

**Solutions**:
- Check RapidAPI dashboard for LinkedIn subscription status
- Verify LinkedIn API quota
- Try setting `LINKEDIN_API_KEY` separately if needed

### "LinkedIn API error"

**Possible causes**:
1. LinkedIn API endpoint changed
2. API key invalid for LinkedIn
3. Rate limit on LinkedIn API

**Solutions**:
- Check RapidAPI dashboard → LinkedIn Jobs API → verify subscription
- Check LinkedIn API rate limits
- Verify API key is correct

### Still seeing Indeed errors

**If you set `USE_LINKEDIN_ONLY = true` but still see Indeed errors**:
1. Make sure you saved the file
2. Restart your Streamlit app completely
3. Clear browser cache and refresh
4. Check that the setting is `true` (not `"true"` or `True`)

## When Your Indeed Quota Resets

If your Indeed quota resets (e.g., monthly reset), you can:

1. **Disable LinkedIn-only mode**:
   ```toml
   USE_LINKEDIN_ONLY = false
   ```

2. **Or keep automatic fallback enabled**:
   ```toml
   SKIP_INDEED_IF_QUOTA_EXCEEDED = true
   ```
   This way, it will try Indeed first, and only use LinkedIn if Indeed fails.

## Summary

| Configuration | Behavior |
|--------------|----------|
| `USE_LINKEDIN_ONLY = true` | Skip Indeed completely, use LinkedIn only |
| `SKIP_INDEED_IF_QUOTA_EXCEEDED = true` | Try Indeed first, auto-switch to LinkedIn on 429 error |
| Both enabled | `USE_LINKEDIN_ONLY` takes precedence (Indeed skipped) |
| Neither enabled | Use Indeed as primary, LinkedIn as fallback (default) |

---

**Remember**: After changing your `secrets.toml`, restart your Streamlit app for changes to take effect!
