/**
 * API Configuration for CareerLens
 * Similar to Streamlit's secrets.toml
 * 
 * IMPORTANT: Never commit actual API keys to git!
 * Use .env file for local development
 * Use environment variables for production
 */

const config = {
  // API Base URL
  // Note: process.env.REACT_APP_* variables are defined in vite.config.js via 'define'
  apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  
  // Use Mock API (for development without backend)
  useMockApi: process.env.REACT_APP_USE_MOCK_API === 'true' || !process.env.REACT_APP_API_URL,
  
  // API Keys (similar to Streamlit secrets)
  apiKeys: {
    // Azure OpenAI API Key (for resume generation and analysis)
    azureOpenAI: {
      apiKey: process.env.REACT_APP_AZURE_OPENAI_API_KEY || '',
      endpoint: process.env.REACT_APP_AZURE_OPENAI_ENDPOINT || '',
    },
    
    // RapidAPI Key (for job scraping)
    rapidAPI: {
      apiKey: process.env.REACT_APP_RAPIDAPI_KEY || '',
    },
    
    // Backend API Key (if your backend requires authentication)
    backend: {
      apiKey: process.env.REACT_APP_BACKEND_API_KEY || '',
    },
  },
  
  // Feature Flags
  features: {
    enableResumeUpload: true,
    enableJobMatching: true,
    enableResumeGeneration: true,
  },
};

// Validate required API keys
export const validateConfig = () => {
  const errors = [];
  
  if (!config.useMockApi) {
    if (!config.apiUrl) {
      errors.push('REACT_APP_API_URL is required when not using mock API');
    }
    
    // Add validation for specific API keys if needed
    // if (config.features.enableResumeGeneration && !config.apiKeys.azureOpenAI.apiKey) {
    //   errors.push('REACT_APP_AZURE_OPENAI_API_KEY is required for resume generation');
    // }
  }
  
  if (errors.length > 0) {
    console.warn('API Configuration Warnings:', errors);
  }
  
  return {
    isValid: errors.length === 0,
    errors,
  };
};

export default config;
