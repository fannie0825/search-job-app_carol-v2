# Rate Limit Optimization Guide

## Summary

This document describes the optimizations implemented to reduce API rate limit errors (429) when generating embeddings.

## ✅ Vector Store Status

**ChromaDB is installed and configured!** The vector store is located at `.chroma_db/` and is being used to:
- Cache job embeddings (persistent storage)
- Cache query embeddings (new feature)
- Avoid redundant API calls for previously embedded content

## 🚀 Optimizations Implemented

### 1. **Reduced Default Batch Size**
- **Before**: 50 embeddings per batch
- **After**: 20 embeddings per batch (configurable)
- **Impact**: Lower burst API calls, more manageable rate limits

### 2. **Rate Limiting & Throttling**
- **Minimum delay between requests**: 100ms
- **Delay between batches**: 1 second (configurable)
- **Rate limit detection**: Automatically detects 429 errors and adjusts behavior
- **Automatic backoff**: Increases delays when rate limits are encountered

### 3. **Query Embedding Caching**
- Query embeddings are now cached in ChromaDB
- Repeated searches with the same query use cached embeddings
- **Impact**: Eliminates redundant API calls for identical queries

### 4. **Intelligent Fallback**
- **Skill matching**: Automatically falls back to string-based matching when rate limits are hit
- **Resume matching**: Returns 0.0 score when rate limited (avoids further API calls)
- **Batch processing**: Automatically reduces batch size when rate limits are detected

### 5. **Better Error Handling**
- Graceful degradation when rate limits are hit
- Clear user feedback about rate limit status
- Automatic retry with exponential backoff (existing feature)

## ⚙️ Configuration Options

You can configure rate limiting behavior via environment variables or Streamlit secrets:

### Environment Variables

```bash
# Batch size for embeddings (default: 20, minimum: 5)
EMBEDDING_BATCH_SIZE=15

# Delay between batches in seconds (default: 1, minimum: 0)
EMBEDDING_BATCH_DELAY=2

# Delay when rate limited in seconds (default: 2, minimum: 1)
EMBEDDING_RATE_LIMIT_DELAY=3

# Maximum jobs to index (default: 50, minimum: 30)
MAX_JOBS_TO_INDEX=40
```

### Streamlit Secrets

Add to `.streamlit/secrets.toml`:

```toml
EMBEDDING_BATCH_SIZE = 15
EMBEDDING_BATCH_DELAY = 2
EMBEDDING_RATE_LIMIT_DELAY = 3
MAX_JOBS_TO_INDEX = 40
```

## 📊 How It Works

### Normal Operation
1. Jobs are embedded in batches of 20 (configurable)
2. 1-second delay between batches
3. Query embeddings are cached after first use
4. Skill matching uses embeddings when available

### When Rate Limited (429)
1. **Detection**: System detects 429 status code
2. **Flag Set**: `rate_limit_encountered` flag is set
3. **Automatic Adjustments**:
   - Batch size reduced by 50%
   - Delays increased between requests
   - Skill matching falls back to string-based
   - Resume matching returns 0.0 to avoid more calls
4. **Recovery**: Flag resets after successful API call

### Vector Store Benefits
- **Job Embeddings**: Stored permanently, only new jobs need embedding
- **Query Embeddings**: Cached for repeated searches
- **Persistent**: Survives app restarts
- **Location**: `.chroma_db/` directory in your workspace

## 🎯 Recommendations

### For High Rate Limits (e.g., 1000+ requests/minute)
```bash
EMBEDDING_BATCH_SIZE=30
EMBEDDING_BATCH_DELAY=0.5
```

### For Low Rate Limits (e.g., 100 requests/minute)
```bash
EMBEDDING_BATCH_SIZE=10
EMBEDDING_BATCH_DELAY=2
EMBEDDING_RATE_LIMIT_DELAY=5
```

### For Very Low Rate Limits (e.g., 20 requests/minute)
```bash
EMBEDDING_BATCH_SIZE=5
EMBEDDING_BATCH_DELAY=3
EMBEDDING_RATE_LIMIT_DELAY=10
MAX_JOBS_TO_INDEX=30
```

## 🔍 Monitoring

The app will show:
- Progress indicators during embedding generation
- Warnings when rate limits are detected
- Batch numbers and progress (e.g., "batch 2/5")
- Automatic fallback messages

## 🛠️ Troubleshooting

### Still Getting Rate Limit Errors?

1. **Reduce batch size further**:
   ```bash
   EMBEDDING_BATCH_SIZE=10
   ```

2. **Increase delays**:
   ```bash
   EMBEDDING_BATCH_DELAY=3
   EMBEDDING_RATE_LIMIT_DELAY=5
   ```

3. **Reduce number of jobs indexed**:
   ```bash
   MAX_JOBS_TO_INDEX=30
   ```

4. **Check your API quota**:
   - Azure OpenAI has tier-based rate limits
   - Free tier: Very limited
   - Pay-as-you-go: Higher limits
   - Check your Azure portal for current limits

5. **Wait and retry**:
   - Rate limits are often time-based (e.g., per minute)
   - Wait a few minutes before retrying

### Vector Store Not Working?

1. **Check permissions**: Ensure write access to `.chroma_db/` directory
2. **Check disk space**: ChromaDB needs disk space for storage
3. **Check logs**: Look for ChromaDB initialization warnings in Streamlit

## 📝 Technical Details

### Rate Limiting Implementation
- **Request throttling**: Minimum 100ms between individual requests
- **Batch delays**: Configurable delay between batch API calls
- **Exponential backoff**: Existing retry logic with exponential delays
- **State tracking**: Tracks rate limit status across requests

### Vector Store Usage
- **Collection name**: `job_embeddings`
- **Distance metric**: Cosine similarity
- **Storage**: Persistent client with local file storage
- **Query caching**: MD5 hash of query text used as ID

### Fallback Mechanisms
- **String-based skill matching**: Used when embeddings unavailable
- **Graceful degradation**: App continues to function with reduced features
- **User feedback**: Clear messages about what's happening

## 🎉 Benefits

1. **Reduced API Calls**: Caching eliminates redundant requests
2. **Better Rate Limit Handling**: Automatic detection and adjustment
3. **Improved User Experience**: Clear feedback and graceful degradation
4. **Cost Savings**: Fewer API calls = lower costs
5. **Faster Searches**: Cached queries are instant

## 📚 Additional Resources

- [Azure OpenAI Rate Limits](https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
