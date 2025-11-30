import React from 'react';
import { ExternalLink, Building2, MapPin, Briefcase } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';

const JobList = ({ jobs = null, loading = false }) => {
  const defaultJobs = [
    {
      id: 'job_1',
      title: 'Senior Software Engineer - FinTech',
      company: 'HSBC Digital',
      location: 'Central, Hong Kong',
      jobUrl: 'https://indeed.com/viewjob?jk=123',
    },
    {
      id: 'job_2',
      title: 'Product Manager - Digital Banking',
      company: 'Standard Chartered',
      location: 'Admiralty, Hong Kong',
      jobUrl: 'https://indeed.com/viewjob?jk=456',
    },
  ];

  // Use provided jobs or fallback to default mock data
  const displayJobs = jobs || defaultJobs;

  if (loading) {
    return (
      <div className="card p-6 bg-bg-card dark:bg-dark-bg-card border-card">
        <div className="flex items-center justify-center py-12">
          <LoadingSpinner size="lg" />
          <span className="ml-3 text-text-body dark:text-dark-text-secondary">
            Fetching jobs from Indeed...
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="card p-6 bg-bg-card dark:bg-dark-bg-card border-card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-text-heading dark:text-dark-text-primary">
          Market Jobs ({displayJobs.length})
        </h2>
        <span className="text-sm text-text-muted dark:text-dark-text-secondary">
          Raw job listings from Indeed
        </span>
      </div>
      
      {displayJobs.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-text-muted dark:text-dark-text-secondary">
            No jobs found. Try adjusting your search parameters.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {displayJobs.map((job, index) => {
            // Handle different job data structures
            const jobId = job.id || job.jobId || `job_${index}`;
            const jobTitle = job.title || job.jobTitle || 'Untitled Position';
            const company = job.company || job.companyName || '';
            const location = job.location || job.jobLocation || '';
            const jobUrl = job.jobUrl || job.url || job.link || '';
            const description = job.description || job.summary || '';
            
            return (
              <div
                key={jobId}
                className="border border-gray-200 dark:border-dark-border rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-dark-bg-main transition-colors"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-text-heading dark:text-dark-text-primary mb-2">
                      {jobTitle}
                    </h3>
                    
                    <div className="flex flex-wrap items-center gap-4 text-sm text-text-body dark:text-dark-text-secondary">
                      {company && (
                        <div className="flex items-center gap-1.5">
                          <Building2 className="w-4 h-4" />
                          <span>{company}</span>
                        </div>
                      )}
                      
                      {location && (
                        <div className="flex items-center gap-1.5">
                          <MapPin className="w-4 h-4" />
                          <span>{location}</span>
                        </div>
                      )}
                    </div>
                    
                    {description && (
                      <p className="text-sm text-text-muted dark:text-dark-text-secondary mt-2 line-clamp-2">
                        {description}
                      </p>
                    )}
                  </div>
                  
                  {jobUrl && (
                    <a
                      href={jobUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 text-accent hover:text-accent-dark font-medium text-sm whitespace-nowrap"
                    >
                      <ExternalLink className="w-4 h-4" />
                      {jobUrl.includes('linkedin.com') ? 'View on LinkedIn' : 'View on Indeed'}
                    </a>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default JobList;
