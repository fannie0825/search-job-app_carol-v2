# API Documentation

This document describes all the APIs used in the application.

## 📡 APIs Used

The application uses **3 main APIs**:

### 1. **Azure OpenAI API** (Primary AI Service)

Used for two purposes:

#### A. Text Embeddings API
- **Purpose**: Semantic job search (vector embeddings)
- **Endpoint**: `{endpoint}/deployments/text-embedding-3-small/embeddings`
- **Model**: `text-embedding-3-small`
- **API Version**: `2024-02-01`
- **Authentication**: API Key (via `api-key` header)
- **Usage**: 
  - Converts job descriptions into vector embeddings
  - Converts user search queries into embeddings
  - Enables semantic similarity matching

**Code Location**: `APIMEmbeddingGenerator` class (lines 92-139)

**Example Request**:
```python
POST {endpoint}/deployments/text-embedding-3-small/embeddings?api-version=2024-02-01
Headers:
  api-key: {AZURE_OPENAI_API_KEY}
  Content-Type: application/json
Body:
{
  "input": "software developer python",
  "model": "text-embedding-3-small"
}
```

#### B. Chat Completions API
- **Purpose**: 
  - Generate tailored resumes
  - Extract structured information from uploaded resumes
- **Endpoint**: `{endpoint}/openai/deployments/gpt-4o-mini/chat/completions`
- **Model**: `gpt-4o-mini`
- **API Version**: `2024-02-01`
- **Authentication**: API Key (via `api-key` header)
- **Usage**:
  - Resume generation: Creates tailored resumes based on user profile and job posting
  - Resume parsing: Extracts structured data from uploaded resume text

**Code Location**: `AzureOpenAITextGenerator` class (lines 141-200)

**Example Request (Resume Generation)**:
```python
POST {endpoint}/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-01
Headers:
  api-key: {AZURE_OPENAI_API_KEY}
  Content-Type: application/json
Body:
{
  "messages": [
    {"role": "system", "content": "You are a professional resume writer..."},
    {"role": "user", "content": "Create a tailored resume..."}
  ],
  "max_tokens": 2000,
  "temperature": 0.7
}
```

**Example Request (Resume Parsing)**:
```python
POST {endpoint}/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-01
Headers:
  api-key: {AZURE_OPENAI_API_KEY}
  Content-Type: application/json
Body:
{
  "messages": [
    {"role": "system", "content": "You are a resume parser..."},
    {"role": "user", "content": "Extract structured information from resume..."}
  ],
  "max_tokens": 2000,
  "temperature": 0.3
}
```

### 2. **RapidAPI - Indeed Scraper API** (Job Search)

- **Purpose**: Fetch real job postings from Indeed
- **Endpoint**: `https://indeed-scraper-api.p.rapidapi.com/api/job`
- **Provider**: RapidAPI
- **Authentication**: RapidAPI Key (via `x-rapidapi-key` header)
- **Usage**: Searches and retrieves job listings from Indeed

**Code Location**: `IndeedScraperAPI` class (lines 202-273)

**Example Request**:
```python
POST https://indeed-scraper-api.p.rapidapi.com/api/job
Headers:
  Content-Type: application/json
  x-rapidapi-host: indeed-scraper-api.p.rapidapi.com
  x-rapidapi-key: {RAPIDAPI_KEY}
Body:
{
  "scraper": {
    "maxRows": 15,
    "query": "software developer",
    "location": "Hong Kong",
    "jobType": "fulltime",
    "radius": "50",
    "sort": "relevance",
    "fromDays": "7",
    "country": "hk"
  }
}
```

## 🔑 API Keys Required

All API keys are stored in `.streamlit/secrets.toml`:

```toml
AZURE_OPENAI_API_KEY = "your-azure-openai-api-key"
AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/"
RAPIDAPI_KEY = "your-rapidapi-key"
```

## 📊 API Usage Summary

| API | Purpose | Model/Service | Cost |
|-----|---------|---------------|------|
| Azure OpenAI Embeddings | Semantic search | text-embedding-3-small | Pay-per-token |
| Azure OpenAI Chat | Resume generation & parsing | gpt-4o-mini | Pay-per-token |
| RapidAPI Indeed Scraper | Job search | Indeed Scraper API | Subscription-based |

## 🔧 API Configuration

### Azure OpenAI Setup
1. Create Azure OpenAI resource in Azure Portal
2. Deploy models:
   - `text-embedding-3-small` (for embeddings)
   - `gpt-4o-mini` (for text generation)
3. Get API key and endpoint from Azure Portal
4. Update deployment names in code if different

### RapidAPI Setup
1. Sign up at [RapidAPI](https://rapidapi.com)
2. Subscribe to [Indeed Scraper API](https://rapidapi.com/indeed-scraper-api/api/indeed-scraper-api)
3. Get your RapidAPI key from dashboard

## 📝 API Endpoints Used

### Azure OpenAI Endpoints

1. **Embeddings Endpoint**:
   ```
   {endpoint}/deployments/text-embedding-3-small/embeddings?api-version=2024-02-01
   ```

2. **Chat Completions Endpoint**:
   ```
   {endpoint}/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-01
   ```

### RapidAPI Endpoint

1. **Indeed Scraper Endpoint**:
   ```
   https://indeed-scraper-api.p.rapidapi.com/api/job
   ```

## 🛠️ HTTP Methods

- **POST**: All API calls use POST method
- **Headers**: JSON content type, API key authentication
- **Timeout**: 
  - Embeddings: 30 seconds
  - Chat completions: 60 seconds
  - Job search: 60 seconds

## 🔄 API Call Flow

### Resume Generation Flow:
```
User Profile + Job Posting 
  → Azure OpenAI Chat API 
  → Tailored Resume
```

### Resume Parsing Flow:
```
Uploaded Resume File 
  → Extract Text (PDF/DOCX/TXT) 
  → Azure OpenAI Chat API 
  → Structured Profile Data
```

### Job Search Flow:
```
User Query 
  → RapidAPI Indeed Scraper 
  → Job Listings
```

### Semantic Search Flow:
```
Job Listings 
  → Azure OpenAI Embeddings 
  → Vector Database 
  → User Query Embedding 
  → Cosine Similarity 
  → Ranked Results
```

## ⚠️ Error Handling

All API calls include:
- Try-catch blocks for exception handling
- HTTP status code checking
- User-friendly error messages
- Graceful fallbacks where possible

## 📚 Additional Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [RapidAPI Indeed Scraper](https://rapidapi.com/indeed-scraper-api/api/indeed-scraper-api)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

---

**Last Updated**: 2025-11-28
