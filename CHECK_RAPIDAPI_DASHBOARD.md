# How to Check Your RapidAPI Dashboard

This guide will help you verify your RapidAPI subscription, check your rate limits, and understand why you might be getting 429 errors.

## Step 1: Log into RapidAPI

1. Go to [https://rapidapi.com](https://rapidapi.com)
2. Click **"Log In"** in the top right corner
3. Enter your credentials and sign in

## Step 2: Check Your Subscription Status

1. Once logged in, click on your **profile icon** (top right)
2. Select **"My Apps"** or **"Dashboard"**
3. Look for **"Billing"** or **"Subscription"** in the menu
4. Check your current subscription tier:
   - **Free Tier**: Usually 3-5 requests/minute, 100-500 requests/month
   - **Basic Tier**: Usually 10-20 requests/minute, 1,000-5,000 requests/month
   - **Pro Tier**: Usually 100+ requests/minute, 10,000+ requests/month

## Step 3: Check API Usage and Rate Limits

### Method 1: Through API Dashboard

1. Go to **"My APIs"** or **"Dashboard"**
2. Find **"Indeed Scraper API"** in your subscribed APIs
3. Click on it to see:
   - **Current usage** (requests made today/this month)
   - **Rate limits** (requests per minute, requests per day/month)
   - **Remaining quota** (how many requests you have left)

### Method 2: Through Billing/Usage Page

1. Click on your **profile icon** → **"Billing"** or **"Usage"**
2. You'll see:
   - **Total API calls** made
   - **Rate limit status** for each API
   - **Quota remaining** for the current period

## Step 4: Verify Your API Key

1. Go to **"My Apps"** or **"Dashboard"**
2. Click on **"Security"** or **"API Keys"**
3. Verify your API key is active and not expired
4. If needed, you can regenerate your key (but remember to update it in your `.streamlit/secrets.toml`)

## Step 5: Check Specific API Limits

1. Navigate to the **Indeed Scraper API** page:
   - Search for "Indeed Scraper API" in RapidAPI
   - Or go directly: [https://rapidapi.com/indeed-scraper-api/api/indeed-scraper-api](https://rapidapi.com/indeed-scraper-api/api/indeed-scraper-api)
2. Click on **"Pricing"** or **"Plans"** tab
3. Check your current plan's limits:
   - **Requests per minute** (RPM)
   - **Requests per month** (RPM)
   - **Rate limit window** (usually 60 seconds)

## Step 6: Check for 429 Errors in Dashboard

1. Go to **"My Apps"** → **"Analytics"** or **"Logs"**
2. Look for:
   - **Error logs** showing 429 status codes
   - **Rate limit violations** or warnings
   - **Peak usage times** when you hit limits

## What to Look For

### ✅ Good Signs:
- Subscription is **active** (not expired)
- You have **quota remaining** for the month
- Your **requests per minute** limit matches what you set in `RAPIDAPI_MAX_REQUESTS_PER_MINUTE`
- No recent **429 errors** in the logs

### ⚠️ Warning Signs:
- Subscription is **expired** or **inactive**
- **Quota exhausted** for the current month
- **Rate limit** is lower than expected (e.g., you thought it was 10/min but it's actually 3/min)
- Many **429 errors** in recent logs
- **API key** is invalid or expired

## Common Issues and Solutions

### Issue 1: "I'm on Free Tier but getting 429 errors"
**Solution**: Free tier typically allows only **3 requests per minute**. Make sure you have:
```toml
RAPIDAPI_MAX_REQUESTS_PER_MINUTE = 3
```
in your `.streamlit/secrets.toml`

### Issue 2: "I upgraded but still getting 429 errors"
**Solution**: 
1. Verify your upgrade is active in the dashboard
2. Update `RAPIDAPI_MAX_REQUESTS_PER_MINUTE` to match your new tier
3. Wait a few minutes for the upgrade to propagate

### Issue 3: "My quota shows 0 remaining"
**Solution**: 
- You've used all your monthly quota
- Wait until the next billing cycle, or
- Upgrade to a higher tier with more quota

### Issue 4: "I can't find my rate limits"
**Solution**: 
- Check the API's **"Pricing"** page on RapidAPI
- Look in **"Billing"** → **"Usage"** section
- Contact RapidAPI support if still unclear

## Quick Checklist

- [ ] Logged into RapidAPI dashboard
- [ ] Verified subscription is active
- [ ] Checked requests per minute limit
- [ ] Checked monthly quota remaining
- [ ] Verified API key is valid
- [ ] Updated `RAPIDAPI_MAX_REQUESTS_PER_MINUTE` in secrets.toml to match your tier
- [ ] Checked for 429 errors in logs

## Need Help?

If you're still experiencing 429 errors after checking everything:

1. **Contact RapidAPI Support**: 
   - Go to RapidAPI → Help/Support
   - Explain your subscription tier and the 429 errors

2. **Check Your Configuration**:
   - Verify `RAPIDAPI_MAX_REQUESTS_PER_MINUTE` matches your tier
   - Make sure `RAPIDAPI_KEY` is correct in `.streamlit/secrets.toml`

3. **Test with Lower Rate**:
   - Try setting `RAPIDAPI_MAX_REQUESTS_PER_MINUTE = 1` temporarily
   - If this works, your tier might have lower limits than expected

## Example: Finding Your Rate Limit

1. Go to [https://rapidapi.com/indeed-scraper-api/api/indeed-scraper-api](https://rapidapi.com/indeed-scraper-api/api/indeed-scraper-api)
2. Click **"Pricing"** tab
3. Find your subscription tier (Free/Basic/Pro)
4. Look for **"Requests per minute"** or **"RPM"**
5. Set that value in your `.streamlit/secrets.toml`:
   ```toml
   RAPIDAPI_MAX_REQUESTS_PER_MINUTE = 3  # Replace with your actual limit
   ```

---

**Remember**: The rate limiter in the code will now automatically enforce this limit, so make sure the value matches what RapidAPI shows in your dashboard!
