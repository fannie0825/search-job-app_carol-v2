/**
 * API Service for CareerLens
 * Handles all API calls to backend services
 */

import config from '../config/api.config';

const API_BASE_URL = config.apiUrl;
const USE_MOCK_API = config.useMockApi;

// Import mock API for development
import mockApiServiceModule from './mockApi';
const mockApiService = USE_MOCK_API ? mockApiServiceModule.default : null;

class ApiService {
  // Use mock API if enabled or if API URL is not set
  _useMock() {
    return USE_MOCK_API && mockApiService !== null;
  }
  /**
   * Upload resume file
   */
  async uploadResume(file) {
    if (this._useMock()) {
      return mockApiService.uploadResume(file);
    }
    const formData = new FormData();
    formData.append('resume', file);

    const headers = {};
    if (config.apiKeys.backend.apiKey) {
      headers['X-API-Key'] = config.apiKeys.backend.apiKey;
    }

    const response = await fetch(`${API_BASE_URL}/resume/upload`, {
      method: 'POST',
      headers,
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Extract profile from resume
   * 
   * Technical Operation: Profile Extraction (GPT-4o)
   * - Triggered by Upload: Automatically called after resume upload
   * - Unchanged: Remains the first required AI call
   * - Necessary: Must happen before any job analysis
   */
  async extractProfile(resumeId) {
    if (this._useMock()) {
      return mockApiService.extractProfile(resumeId);
    }
    const headers = {
      'Content-Type': 'application/json',
    };
    if (config.apiKeys.backend.apiKey) {
      headers['X-API-Key'] = config.apiKeys.backend.apiKey;
    }

    const response = await fetch(`${API_BASE_URL}/resume/${resumeId}/extract`, {
      method: 'POST',
      headers,
    });

    if (!response.ok) {
      throw new Error(`Profile extraction failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Analyze profile and get market positioning
   */
  async analyzeProfile(profileData, filters) {
    if (this._useMock()) {
      return mockApiService.analyzeProfile(profileData, filters);
    }
    const headers = {
      'Content-Type': 'application/json',
    };
    if (config.apiKeys.backend.apiKey) {
      headers['X-API-Key'] = config.apiKeys.backend.apiKey;
    }

    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        profile: profileData,
        filters: filters,
      }),
    });

    if (!response.ok) {
      throw new Error(`Analysis failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get job matches with AI-powered ranking
   * 
   * Technical Operation: Embedding Generation + Semantic Search
   * - Delayed and Gated: Only triggered by "Analyze and Rank Top 15 Matches" button
   * - High Load Operations:
   *   1. Semantic Indexing (Job Embeddings via Azure OpenAI)
   *   2. Semantic Search (Cosine Similarity)
   *   3. Skill Matching
   * - Rate Limit Management: Second burst of API calls (Azure Embedding API)
   * - UX: User commits to 10-15 second AI analysis only when ready
   */
  async getJobMatches(profileData, filters, topK = 15) {
    if (this._useMock()) {
      return mockApiService.getJobMatches(profileData, filters);
    }
    const headers = {
      'Content-Type': 'application/json',
    };
    if (config.apiKeys.backend.apiKey) {
      headers['X-API-Key'] = config.apiKeys.backend.apiKey;
    }

    const response = await fetch(`${API_BASE_URL}/jobs/matches`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        profile: profileData,
        filters: filters,
        top_k: topK,
      }),
    });

    if (!response.ok) {
      throw new Error(`Job matching failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Generate tailored resume
   */
  async generateTailoredResume(profileData, jobId) {
    if (this._useMock()) {
      return mockApiService.generateTailoredResume(profileData, jobId);
    }
    const headers = {
      'Content-Type': 'application/json',
    };
    if (config.apiKeys.backend.apiKey) {
      headers['X-API-Key'] = config.apiKeys.backend.apiKey;
    }

    const response = await fetch(`${API_BASE_URL}/resume/tailor`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        profile: profileData,
        job_id: jobId,
      }),
    });

    if (!response.ok) {
      throw new Error(`Resume generation failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get market positioning metrics
   * 
   * Technical Operation: Market Analysis (GPT-4o)
   * - Based on resume/profile only, NOT job list
   * - Called after job fetch to show market insights
   * - Does NOT trigger job embeddings (that's only in getJobMatches)
   * - Uses AI for resume analysis but not for job matching
   */
  async getMarketPositioning(profileData, filters) {
    if (this._useMock()) {
      return mockApiService.getMarketPositioning(profileData, filters);
    }
    const headers = {
      'Content-Type': 'application/json',
    };
    if (config.apiKeys.backend.apiKey) {
      headers['X-API-Key'] = config.apiKeys.backend.apiKey;
    }

    const response = await fetch(`${API_BASE_URL}/market/positioning`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        profile: profileData,
        filters: filters,
      }),
    });

    if (!response.ok) {
      throw new Error(`Market positioning failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Fetch jobs from Indeed (simple fetch, no embeddings)
   * 
   * Technical Operation: Job Fetch (Indeed API)
   * - Isolated and Gated: Triggered by "Fetch Market Jobs" button
   * - NO Embedding Generation: This endpoint only calls Indeed API
   * - Rate Limit Management: Small burst of API calls (just Indeed API)
   * - UX: User waits ~5 seconds for job titles
   */
  async fetchJobs(filters) {
    if (this._useMock()) {
      return mockApiService.fetchJobs(filters);
    }
    const headers = {
      'Content-Type': 'application/json',
    };
    if (config.apiKeys.backend.apiKey) {
      headers['X-API-Key'] = config.apiKeys.backend.apiKey;
    }

    const response = await fetch(`${API_BASE_URL}/jobs/fetch`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        keywords: filters.keywords || '',
        location: filters.location || 'Hong Kong',
        jobType: filters.jobType || 'fulltime',
        numJobs: filters.numJobs || 25,
        industries: filters.industries || [],
        minSalary: filters.minSalary,
        maxSalary: filters.maxSalary,
      }),
    });

    if (!response.ok) {
      throw new Error(`Job fetching failed: ${response.statusText}`);
    }

    return response.json();
  }
}

export default new ApiService();
