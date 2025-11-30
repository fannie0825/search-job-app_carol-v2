import React, { useState } from 'react';
import { ChevronDown, ChevronUp, FileText, ExternalLink } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';

const JobMatchTable = ({ jobs = null, loading = false, onTailorResume, toast }) => {
  const [expandedRows, setExpandedRows] = useState(new Set([2])); // Row 3 (index 2) expanded by default

  const defaultJobs = [
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
    {
      id: 4,
      rank: 4,
      jobTitle: 'Data Analytics Manager',
      company: 'Deloitte',
      location: 'Central, HK',
      matchScore: 78,
      fitType: 'Semantic / Skill-Overlap',
      whyFit: 'Good overlap in analytics skills, but requires more hands-on data engineering experience.',
      missingSkill: 'Apache Spark'
    },
    {
      id: 5,
      rank: 5,
      jobTitle: 'ESG Strategy Consultant',
      company: 'EY Hong Kong',
      location: 'Central, HK',
      matchScore: 75,
      fitType: 'Semantic / Skill-Overlap',
      whyFit: 'Relevant consulting background, but ESG-specific knowledge would be beneficial.',
      missingSkill: 'ESG Reporting Standards'
    }
  ];

  // Use provided jobs or fallback to default mock data
  const displayJobs = jobs || defaultJobs;

  const toggleRow = (id) => {
    const newExpanded = new Set(expandedRows);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedRows(newExpanded);
  };

  const handleTailorResume = async (job) => {
    if (onTailorResume) {
      try {
        await onTailorResume(job);
      } catch (error) {
        console.error('Error tailoring resume:', error);
      }
    } else {
      console.log(`Generating tailored resume for: ${job.jobTitle} at ${job.company}`);
      toast?.info(`Generating tailored resume for ${job.jobTitle}...`);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 85) return 'bg-status-success';
    if (score >= 70) return 'bg-status-warning';
    return 'bg-status-error';
  };

  if (loading) {
    return (
      <div className="card p-6 bg-bg-card dark:bg-dark-bg-card border-card">
        <div className="flex items-center justify-center py-12">
          <LoadingSpinner size="lg" />
          <span className="ml-3 text-text-body dark:text-dark-text-secondary">
            Loading job matches...
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="card p-6 bg-bg-card dark:bg-dark-bg-card border-card">
      <h2 className="text-xl font-bold text-text-heading dark:text-dark-text-primary mb-6">
        Smart Ranked Matches
      </h2>
      
      {displayJobs.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-text-muted dark:text-dark-text-secondary">
            No job matches found. Try adjusting your filters.
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200 dark:border-dark-border">
              <th className="text-left py-3 px-4 text-sm font-semibold text-text-muted dark:text-dark-text-secondary uppercase tracking-wide">
                Rank
              </th>
              <th className="text-left py-3 px-4 text-sm font-semibold text-text-muted dark:text-dark-text-secondary uppercase tracking-wide">
                Job Title
              </th>
              <th className="text-left py-3 px-4 text-sm font-semibold text-text-muted dark:text-dark-text-secondary uppercase tracking-wide">
                Company
              </th>
              <th className="text-left py-3 px-4 text-sm font-semibold text-text-muted dark:text-dark-text-secondary uppercase tracking-wide">
                Location (HK)
              </th>
              <th className="text-left py-3 px-4 text-sm font-semibold text-text-muted dark:text-dark-text-secondary uppercase tracking-wide">
                Match Score
              </th>
              <th className="text-left py-3 px-4 text-sm font-semibold text-text-muted dark:text-dark-text-secondary uppercase tracking-wide">
                Fit Type
              </th>
              <th className="text-left py-3 px-4 text-sm font-semibold text-text-muted dark:text-dark-text-secondary uppercase tracking-wide">
                Action
              </th>
            </tr>
          </thead>
          <tbody>
            {displayJobs.map((job) => {
              const isExpanded = expandedRows.has(job.id);
              return (
                <React.Fragment key={job.id}>
                  <tr
                    className="border-b border-gray-100 dark:border-dark-border hover:bg-gray-50 dark:hover:bg-dark-bg-main cursor-pointer transition-colors"
                    onClick={() => toggleRow(job.id)}
                  >
                    <td className="py-4 px-4">
                      <div className="flex items-center gap-2">
                        <span className="text-lg font-bold text-text-heading dark:text-dark-text-primary">
                          #{job.rank}
                        </span>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            toggleRow(job.id);
                          }}
                          className="text-text-muted dark:text-dark-text-secondary hover:text-accent transition-colors"
                        >
                          {isExpanded ? (
                            <ChevronUp className="w-4 h-4" />
                          ) : (
                            <ChevronDown className="w-4 h-4" />
                          )}
                        </button>
                      </div>
                    </td>
                    <td className="py-4 px-4">
                      <div className="font-semibold text-text-heading dark:text-dark-text-primary">
                        {job.jobTitle}
                      </div>
                    </td>
                    <td className="py-4 px-4 text-text-body dark:text-dark-text-secondary">
                      {job.company}
                    </td>
                    <td className="py-4 px-4 text-text-body dark:text-dark-text-secondary">
                      {job.location}
                    </td>
                    <td className="py-4 px-4">
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-gray-200 dark:bg-dark-bg-card rounded-full h-2 min-w-[60px]">
                          <div
                            className={`h-2 rounded-full ${getScoreColor(job.matchScore)}`}
                            style={{ width: `${job.matchScore}%` }}
                          />
                        </div>
                        <span className="text-sm font-semibold text-text-heading dark:text-dark-text-primary min-w-[40px]">
                          {job.matchScore}%
                        </span>
                      </div>
                    </td>
                    <td className="py-4 px-4">
                      <span className="text-xs text-text-muted dark:text-dark-text-secondary">
                        {job.fitType}
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleTailorResume(job);
                        }}
                        className="btn-secondary btn-secondary-dark text-sm py-2 px-4 flex items-center gap-2"
                      >
                        <FileText className="w-4 h-4" />
                        Tailor Resume
                      </button>
                    </td>
                  </tr>
                  {isExpanded && (
                    <tr>
                      <td colSpan="7" className="py-4 px-4">
                        <div className="bg-gray-50 dark:bg-dark-bg-main rounded-lg p-4 border-l-4 border-accent">
                          <div className="space-y-3">
                            <div>
                              <h4 className="text-sm font-semibold text-text-heading dark:text-dark-text-primary mb-1">
                                Why this fits:
                              </h4>
                              <p className="text-sm text-text-body dark:text-dark-text-secondary">
                                {job.whyFit}
                              </p>
                            </div>
                            <div>
                              <h4 className="text-sm font-semibold text-status-warning dark:text-status-warning mb-1">
                                Missing skill:
                              </h4>
                              <p className="text-sm text-text-body dark:text-dark-text-secondary">
                                {job.missingSkill}
                              </p>
                            </div>
                            <div className="pt-2">
                              {(job.jobUrl || job.url || job.link) ? (
                                <a
                                  href={job.jobUrl || job.url || job.link}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-sm text-accent hover:text-accent-dark font-medium flex items-center gap-1"
                                >
                                  View Full Job Description
                                  <ExternalLink className="w-3 h-3" />
                                </a>
                              ) : (
                                <span className="text-sm text-text-muted dark:text-dark-text-secondary">
                                  Job URL not available
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
      )}
    </div>
  );
};

export default JobMatchTable;
