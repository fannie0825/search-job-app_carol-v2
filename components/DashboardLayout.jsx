import React, { useState, useEffect } from 'react';
import { Menu } from 'lucide-react';
import Sidebar from './Sidebar';
import MarketPositionCards from './MarketPositionCards';
import JobMatchTable from './JobMatchTable';
import JobList from './JobList';
import ToastContainer from './Toast';
import LoadingOverlay from './LoadingSpinner';
import { useToast } from '../hooks/useToast';
import ApiService from '../services/api';

const DashboardLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [loading, setLoading] = useState(false);
  const [profileData, setProfileData] = useState(null);
  const [marketPositioning, setMarketPositioning] = useState(null);
  const [jobMatches, setJobMatches] = useState(null);
  const [rawJobs, setRawJobs] = useState(null);
  const [hasFetchedJobs, setHasFetchedJobs] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const { toasts, removeToast, success, error, warning, info } = useToast();

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 1024); // lg breakpoint
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const handleFileUploaded = async (fileResult, profile) => {
    if (profile) {
      setProfileData(profile);
      success('Profile extracted from resume successfully!');
    }
  };

  /**
   * Step 1: Fetch Market Jobs
   * 
   * Technical Operations:
   * - Job Fetch (Indeed API): Isolated and gated, no embeddings
   * - Market Positioning: Based on resume only (GPT-4o), not job list
   * - Rate Limit: Small burst (Indeed API only)
   * - UX: ~5 second wait for job titles
   */
  const handleFetchJobs = async (filters) => {
    if (!profileData) {
      warning('Please upload a resume first');
      return;
    }

    setLoading(true);
    setIsAnalyzing(false);
    try {
      // Step 1: Fetch jobs from Indeed (NO embeddings - just raw job data)
      const jobsResult = await ApiService.fetchJobs(filters);
      const jobs = Array.isArray(jobsResult) ? jobsResult : (jobsResult?.jobs || []);
      setRawJobs(jobs);
      setHasFetchedJobs(true);

      // Get market positioning based on resume only (NOT job list)
      // This uses GPT-4o for resume analysis but does NOT trigger job embeddings
      const positioning = await ApiService.getMarketPositioning(profileData, filters);
      setMarketPositioning(positioning);

      // Clear ranked matches until user clicks "Analyze and Rank"
      setJobMatches(null);

      success(`Fetched ${jobs.length} jobs from Indeed! Review them below, then click "Analyze and Rank" for AI-powered matching.`);
    } catch (err) {
      console.error('Job fetch error:', err);
      error(err.message || 'Failed to fetch jobs. Please try again.');
      setRawJobs(null);
      setHasFetchedJobs(false);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Step 2: Analyze and Rank Top 15 Matches
   * 
   * Technical Operations (High Load):
   * - Embedding Generation: Semantic Indexing for jobs (Azure OpenAI Embeddings)
   * - Semantic Search: Cosine Similarity matching
   * - Skill Matching: Detailed skill overlap analysis
   * - Rate Limit: Second burst of API calls (Azure Embedding API)
   * - UX: User commits to 10-15 second AI analysis only when ready
   */
  const handleAnalyze = async (filters) => {
    if (!profileData) {
      warning('Please upload a resume first');
      return;
    }

    if (!hasFetchedJobs || !rawJobs || rawJobs.length === 0) {
      warning('Please fetch jobs first using "Fetch Market Jobs" button');
      return;
    }

    setLoading(true);
    setIsAnalyzing(true);
    try {
      // Step 2: Expensive AI processing - THIS is where embeddings happen
      // 1. Semantic Indexing (Job Embeddings via Azure OpenAI)
      // 2. Semantic Search (Cosine Similarity)
      // 3. Skill Matching
      const matches = await ApiService.getJobMatches(profileData, filters, 15);
      // Handle both { jobs: [...] } and [...] formats
      setJobMatches(Array.isArray(matches) ? matches : (matches?.jobs || []));

      success('Analysis complete! Top 15 ranked matches are ready.');
    } catch (err) {
      console.error('Analysis error:', err);
      error(err.message || 'Analysis failed. Please try again.');
      setJobMatches(null);
    } finally {
      setLoading(false);
    }
  };

  const handleTailorResume = async (job) => {
    if (!profileData) {
      warning('Please upload a resume first');
      return;
    }

    // Extract job ID from various possible formats
    const jobId = job.id || job.jobId || job._id || job.originalJob?.id || job.originalJob?.jobId;
    
    if (!jobId) {
      error('Unable to identify job. Please try again.');
      return;
    }

    setLoading(true);
    try {
      info(`Generating tailored resume for ${job.jobTitle || job.title || 'this position'}...`);
      const result = await ApiService.generateTailoredResume(profileData, jobId);
      
      success(`Tailored resume generated for ${job.jobTitle || job.title || 'this position'}!`);
      
      // Handle resume download or display
      if (result.downloadUrl && result.downloadUrl !== '#') {
        window.open(result.downloadUrl, '_blank');
      } else if (result.fileUrl) {
        window.open(result.fileUrl, '_blank');
      } else if (result.url) {
        window.open(result.url, '_blank');
      } else {
        // If no download URL, show success message with instructions
        info('Resume generated successfully! Check your downloads or the generated files section.');
      }
    } catch (err) {
      console.error('Resume generation error:', err);
      error(err.message || 'Failed to generate tailored resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-bg-main dark:bg-dark-bg-main">
      {/* Mobile Header */}
      {isMobile && (
        <header className="lg:hidden fixed top-0 left-0 right-0 z-30 bg-bg-sidebar text-white p-4 flex items-center justify-between shadow-lg">
          <h1 className="text-lg font-bold">CareerLens</h1>
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 hover:bg-navy-light rounded-lg transition-colors"
            aria-label="Toggle sidebar"
          >
            <Menu className="w-6 h-6" />
          </button>
        </header>
      )}

      <div className="flex h-screen overflow-hidden">
        {/* Sidebar */}
        <Sidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          isMobile={isMobile}
          onFileUploaded={handleFileUploaded}
          onFetchJobs={handleFetchJobs}
          onAnalyze={handleAnalyze}
          toast={{ success, error, warning, info }}
        />

        {/* Main Content Area */}
        <main className={`flex-1 overflow-y-auto scrollbar-thin ${
          isMobile ? 'pt-16' : ''
        }`}>
          <div className="max-w-7xl mx-auto p-6 lg:p-8">
            {/* Header */}
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-text-heading dark:text-dark-text-primary mb-2">
                Market Positioning & Smart Matches
              </h1>
              <p className="text-text-muted dark:text-dark-text-secondary">
                AI-powered career insights for the Hong Kong market
              </p>
            </div>

            {/* Market Positioning Cards */}
            <MarketPositionCards data={marketPositioning} />

            {/* Raw Job List (Step 1) */}
            {hasFetchedJobs && rawJobs && (
              <div className="mb-8">
                <JobList jobs={rawJobs} loading={loading} />
              </div>
            )}

            {/* Ranked Job Matches Table (Step 2) */}
            {jobMatches && jobMatches.length > 0 && (
              <div className="mb-8">
                <JobMatchTable
                  jobs={jobMatches}
                  loading={loading}
                  onTailorResume={handleTailorResume}
                  toast={{ success, error, warning, info }}
                />
              </div>
            )}

            {/* Empty State */}
            {!hasFetchedJobs && !jobMatches && (
              <div className="card p-12 bg-bg-card dark:bg-dark-bg-card border-card text-center">
                <p className="text-text-muted dark:text-dark-text-secondary text-lg">
                  Upload your resume and click "Fetch Market Jobs" to get started.
                </p>
              </div>
            )}
          </div>
        </main>
      </div>

      {/* Toast Notifications */}
      <ToastContainer toasts={toasts} onRemove={removeToast} />

      {/* Loading Overlay */}
      {loading && (
        <LoadingOverlay 
          message={isAnalyzing ? "Analyzing and ranking jobs..." : "Fetching jobs from Indeed..."} 
        />
      )}
    </div>
  );
};

export default DashboardLayout;
