# Semantic Job Search & Resume Generator

An AI-powered job search application with intelligent resume generation capabilities. This application helps users find relevant job postings and automatically generates tailored resumes for each position.

## 🌟 Features

### 1. **Semantic Job Search**
- Search jobs from Indeed using keywords and location
- AI-powered semantic matching using Azure OpenAI embeddings
- Intelligent ranking based on job description similarity
- Filter by country, job type, and match score

### 2. **AI-Powered Resume Generation**
- Create personalized resumes tailored to specific job postings
- Automatic keyword optimization for ATS (Applicant Tracking Systems)
- Highlight relevant experience and skills for each position
- Edit and download generated resumes

### 3. **User Profile Management**
- Store your professional information securely
- Include work experience, education, skills, and certifications
- Reuse profile for multiple job applications

### 4. **Direct Job Application**
- Access job posting websites directly
- Generate resume before applying
- Seamless integration with Indeed job links

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Azure OpenAI API account
- RapidAPI account (for Indeed Scraper API)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd workspace
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Streamlit secrets:

Create a `.streamlit/secrets.toml` file in the project root:
```toml
AZURE_OPENAI_API_KEY = "your-azure-openai-api-key"
AZURE_OPENAI_ENDPOINT = "your-azure-openai-endpoint"
RAPIDAPI_KEY = "your-rapidapi-key"
```

4. Run the application:
```bash
streamlit run app.py
```

## 📖 Usage Guide

### Step 1: Set Up Your Profile
1. Navigate to the **"My Profile"** tab
2. Fill in your personal information:
   - Contact details (name, email, phone)
   - Professional summary
   - Work experience
   - Education
   - Skills and certifications
3. Click **"Save Profile"**

### Step 2: Search for Jobs
1. Go to the **"Job Search"** tab
2. Configure search settings in the sidebar:
   - Keywords (e.g., "software developer")
   - Location
   - Country
   - Job type
   - Number of results
3. Click **"Fetch Jobs"**

### Step 3: Find Relevant Matches
1. Enter your ideal job description in the semantic search box
2. Adjust the number of results and minimum match score
3. Click **"Search"** to get AI-ranked results

### Step 4: Generate Tailored Resume
1. Click the **"📄 Resume"** button on any job card
2. Review your profile information
3. Click **"Generate Tailored Resume"**
4. Edit the generated resume if needed
5. Download as TXT or copy to clipboard
6. Click **"Apply to Job"** to visit the job posting

## 🎨 Key Features Explained

### Semantic Search
Uses Azure OpenAI's embedding models to understand the semantic meaning of job descriptions and user queries, providing more relevant matches than keyword-based search.

### Resume Tailoring
The AI analyzes both your profile and the job description to:
- Emphasize relevant experience
- Include job-specific keywords for ATS optimization
- Highlight matching skills
- Format professionally

### Smart Job Matching
Each job is scored based on similarity to your search query, helping you focus on the most relevant opportunities.

## 🔧 Configuration

### Azure OpenAI Setup
1. Deploy `text-embedding-3-small` model for embeddings
2. Deploy `gpt-4o-mini` (or similar) for text generation
3. Update deployment names in `app.py` if different

### API Keys
- **Azure OpenAI**: Get from Azure Portal
- **RapidAPI**: Sign up at https://rapidapi.com/ and subscribe to Indeed Scraper API

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **AI/ML**: Azure OpenAI (embeddings & text generation)
- **Job Data**: Indeed Scraper API (via RapidAPI)
- **Vector Search**: Scikit-learn (cosine similarity)

## 📊 Data Flow

1. **Job Fetching**: Indeed API → Job data with descriptions
2. **Indexing**: Job descriptions → Azure OpenAI embeddings → Vector database
3. **Search**: User query → Embedding → Similarity search → Ranked results
4. **Resume Generation**: User profile + Job description → GPT-4 → Tailored resume

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is provided as-is for educational and personal use.

## 🙏 Acknowledgments

- Azure OpenAI for powerful AI capabilities
- Streamlit for the intuitive web framework
- RapidAPI for job search API access

## 💡 Tips for Best Results

1. **Complete Profile**: Fill out all profile sections for better resume generation
2. **Be Specific**: Use detailed descriptions in your search queries
3. **Review Generated Resumes**: Always review and customize generated resumes
4. **Update Regularly**: Keep your profile current with latest experience
5. **Use Keywords**: Include industry-specific terms in your profile

## 🐛 Troubleshooting

**Issue**: API errors when generating resumes
- **Solution**: Check Azure OpenAI API key and endpoint configuration

**Issue**: No jobs found
- **Solution**: Try broader keywords or different locations

**Issue**: Low match scores
- **Solution**: Adjust minimum score slider or refine search query

## 📞 Support

For issues or questions, please open an issue in the repository.

---

Made with ❤️ using Streamlit and Azure OpenAI
