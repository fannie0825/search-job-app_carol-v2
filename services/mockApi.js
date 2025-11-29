/**
 * Mock API Service for Development
 * Use this when backend API is not available
 */

// Simulate API delay
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const mockApiService = {
  async uploadResume(file) {
    await delay(1500);
    return {
      id: `resume_${Date.now()}`,
      filename: file.name,
      size: file.size,
      uploadedAt: new Date().toISOString(),
    };
  },

  async extractProfile(resumeId) {
    await delay(2000);
    return {
      id: resumeId,
      name: 'John Doe',
      email: 'john.doe@example.com',
      skills: ['JavaScript', 'React', 'Node.js', 'AWS'],
      experience: '5+ years in software development',
      summary: 'Experienced software engineer with expertise in modern web technologies.',
    };
  },

  async analyzeProfile(profileData, filters) {
    await delay(2500);
    return {
      success: true,
      timestamp: new Date().toISOString(),
    };
  },

  async getMarketPositioning(profileData, filters) {
    await delay(2000);
    return {
      salaryBand: 'HK$45k-60k',
      salaryDelta: '+12% vs market avg',
      salaryDescription: 'Your experience aligns with mid-senior level roles',
      topSkillGap: 'Cloud Architecture',
      skillGapDelta: 'High demand in HK',
      skillGapDescription: 'Consider AWS or Azure certifications',
      recommendedAccreditation: 'AWS Certified Solutions Architect',
      accreditationDelta: 'Unlock 15% more roles',
      accreditationDescription: 'Most valued certification in your target market',
    };
  },

  async getJobMatches(profileData, filters) {
    await delay(2000);
    return {
      jobs: [
        {
          id: 1,
          rank: 1,
          jobTitle: 'Senior Product Manager - FinTech',
          company: 'HSBC Digital',
          location: 'Central, HK',
          matchScore: 92,
          fitType: 'Semantic / Skill-Overlap',
          whyFit: 'Strong alignment with your product management experience in financial services and digital transformation projects.',
          missingSkill: 'Blockchain fundamentals'
        },
        {
          id: 2,
          rank: 2,
          jobTitle: 'Cloud Solutions Architect',
          company: 'AWS Hong Kong',
          location: 'Wan Chai, HK',
          matchScore: 88,
          fitType: 'Semantic / Skill-Overlap',
          whyFit: 'Your cloud infrastructure experience matches well, though AWS-specific certifications would strengthen your profile.',
          missingSkill: 'AWS Certified Solutions Architect'
        },
        {
          id: 3,
          rank: 3,
          jobTitle: 'Digital Transformation Lead',
          company: 'PwC Hong Kong',
          location: 'Admiralty, HK',
          matchScore: 85,
          fitType: 'Semantic / Skill-Overlap',
          whyFit: 'Strong semantic match with your project management experience in digital transformation.',
          missingSkill: 'Python'
        },
      ],
    };
  },

  async generateTailoredResume(profileData, jobId) {
    await delay(3000);
    return {
      id: `resume_${Date.now()}`,
      jobId,
      downloadUrl: '#', // In real app, this would be a download URL
      generatedAt: new Date().toISOString(),
    };
  },

  async fetchJobs(filters) {
    await delay(2000);
    // Return raw job listings without ranking or embeddings
    const mockJobs = [
      {
        id: 'job_1',
        title: 'Senior Software Engineer - FinTech',
        company: 'HSBC Digital',
        location: 'Central, Hong Kong',
        jobUrl: 'https://indeed.com/viewjob?jk=123',
        description: 'We are looking for an experienced software engineer...',
      },
      {
        id: 'job_2',
        title: 'Product Manager - Digital Banking',
        company: 'Standard Chartered',
        location: 'Admiralty, Hong Kong',
        jobUrl: 'https://indeed.com/viewjob?jk=456',
        description: 'Join our digital transformation team...',
      },
      {
        id: 'job_3',
        title: 'Cloud Solutions Architect',
        company: 'AWS Hong Kong',
        location: 'Wan Chai, Hong Kong',
        jobUrl: 'https://indeed.com/viewjob?jk=789',
        description: 'Design and implement cloud solutions...',
      },
      {
        id: 'job_4',
        title: 'Data Analytics Manager',
        company: 'Deloitte',
        location: 'Central, Hong Kong',
        jobUrl: 'https://indeed.com/viewjob?jk=101',
        description: 'Lead analytics initiatives for clients...',
      },
      {
        id: 'job_5',
        title: 'ESG Strategy Consultant',
        company: 'EY Hong Kong',
        location: 'Central, Hong Kong',
        jobUrl: 'https://indeed.com/viewjob?jk=102',
        description: 'Help clients develop ESG strategies...',
      },
    ];
    
    return {
      jobs: mockJobs.slice(0, filters.numJobs || 25),
      count: mockJobs.length,
      fetchedAt: new Date().toISOString(),
    };
  },
};

export default mockApiService;
