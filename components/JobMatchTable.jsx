import React, { useState } from 'react';
import { ChevronDown, ChevronUp, FileText, ExternalLink, X, Eye } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';

const JobMatchTable = ({ jobs = null, loading = false, onTailorResume, toast }) => {
  const [expandedRows, setExpandedRows] = useState(new Set());
  const [selectedJob, setSelectedJob] = useState(null);

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

  // Normalize job data structure to handle different backend formats
  const normalizeJob = (job, index) => {
    // Generate a stable ID if missing
    const id = job.id || job.jobId || job._id || `job_${index}`;
    
    return {
      id: String(id), // Ensure ID is always a string for consistent comparison
      rank: job.rank || index + 1,
      jobTitle: job.jobTitle || job.title || job.position || 'Untitled Position',
      company: job.company || job.companyName || job.employer || 'Unknown Company',
      location: job.location || job.jobLocation || job.city || 'Location not specified',
      matchScore: job.matchScore || job.score || job.combined_match_score || 0,
      fitType: job.fitType || job.matchType || 'Semantic / Skill-Overlap',
      whyFit: job.whyFit || job.why_fit || job.matchReason || job.reason || 'Good match based on your profile and experience.',
      missingSkill: job.missingSkill || job.missing_skill || job.skillGap || job.missing_skills?.[0] || 'No significant skill gaps identified.',
      jobUrl: job.jobUrl || job.url || job.link || job.job_url || job.external_url,
      description: job.description || job.summary || job.jobDescription || '',
      skills: job.skills || job.requiredSkills || [],
      salary: job.salary || job.salaryRange || '',
      jobType: job.jobType || job.type || '',
      // Store original job data for resume generation
      originalJob: job,
    };
  };

  // Use provided jobs or fallback to default mock data
  const displayJobs = (jobs || defaultJobs).map((job, index) => normalizeJob(job, index));

  const toggleRow = (id) => {
    const newExpanded = new Set(expandedRows);
    if (newExpanded.has(String(id))) {
      newExpanded.delete(String(id));
    } else {
      newExpanded.add(String(id));
    }
    setExpandedRows(newExpanded);
  };

  const handleViewDetails = (job, e) => {
    if (e) {
      e.stopPropagation();
    }
    setSelectedJob(job);
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
              <th className="sticky left-0 z-10 bg-bg-card dark:bg-dark-bg-card text-left py-3 px-4 text-sm font-semibold text-text-muted dark:text-dark-text-secondary uppercase tracking-wide border-r border-gray-200 dark:border-dark-border shadow-sm">
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
              const isExpanded = expandedRows.has(String(job.id));
              return (
                <React.Fragment key={job.id}>
                  <tr
                    className="group border-b border-gray-100 dark:border-dark-border hover:bg-gray-50 dark:hover:bg-dark-bg-main cursor-pointer transition-colors"
                    onClick={() => toggleRow(job.id)}
                  >
                    <td className="sticky left-0 z-10 bg-bg-card dark:bg-dark-bg-card py-4 px-4 border-r border-gray-200 dark:border-dark-border group-hover:bg-gray-50 dark:group-hover:bg-dark-bg-main transition-colors">
                      <div className="flex items-center gap-2">
                        <span className="text-xl font-bold text-accent dark:text-accent-light">
                          #{job.rank}
                        </span>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            toggleRow(job.id);
                          }}
                          className="text-text-muted dark:text-dark-text-secondary hover:text-accent transition-colors p-1 rounded hover:bg-gray-100 dark:hover:bg-dark-bg-main"
                          aria-label={isExpanded ? "Collapse details" : "Expand details"}
                        >
                          {isExpanded ? (
                            <ChevronUp className="w-5 h-5" />
                          ) : (
                            <ChevronDown className="w-5 h-5" />
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
                      <div className="flex items-center gap-2">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleViewDetails(job, e);
                          }}
                          className="btn-secondary btn-secondary-dark text-sm py-2 px-3 flex items-center gap-1.5"
                          title="View full job details"
                        >
                          <Eye className="w-4 h-4" />
                          Details
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleTailorResume(job);
                          }}
                          className="btn-primary text-sm py-2 px-3 flex items-center gap-1.5"
                          title="Generate tailored resume for this job"
                        >
                          <FileText className="w-4 h-4" />
                          Tailor Resume
                        </button>
                      </div>
                    </td>
                  </tr>
                  {isExpanded && (
                    <tr>
                      <td colSpan="7" className="py-4 px-4">
                        <div className="bg-gray-50 dark:bg-dark-bg-main rounded-lg p-6 border-l-4 border-accent shadow-sm">
                          <div className="space-y-4">
                            {/* Match Analysis Section */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pb-4 border-b border-gray-200 dark:border-dark-border">
                              <div>
                                <h4 className="text-sm font-semibold text-text-heading dark:text-dark-text-primary mb-2 flex items-center gap-2">
                                  <span className="w-2 h-2 rounded-full bg-status-success"></span>
                                  Match Score Breakdown
                                </h4>
                                <div className="space-y-2">
                                  <div className="flex items-center justify-between">
                                    <span className="text-xs text-text-muted dark:text-dark-text-secondary">Overall Match</span>
                                    <span className="text-sm font-bold text-text-heading dark:text-dark-text-primary">{job.matchScore}%</span>
                                  </div>
                                  <div className="w-full bg-gray-200 dark:bg-dark-bg-card rounded-full h-2">
                                    <div
                                      className={`h-2 rounded-full ${getScoreColor(job.matchScore)}`}
                                      style={{ width: `${job.matchScore}%` }}
                                    />
                                  </div>
                                </div>
                              </div>
                              <div>
                                <h4 className="text-sm font-semibold text-text-heading dark:text-dark-text-primary mb-2 flex items-center gap-2">
                                  <span className="w-2 h-2 rounded-full bg-accent"></span>
                                  Fit Type
                                </h4>
                                <p className="text-sm text-text-body dark:text-dark-text-secondary">
                                  {job.fitType}
                                </p>
                              </div>
                            </div>

                            {/* Why This Fits */}
                            {job.whyFit && (
                              <div>
                                <h4 className="text-sm font-semibold text-text-heading dark:text-dark-text-primary mb-2 flex items-center gap-2">
                                  <span className="w-2 h-2 rounded-full bg-status-success"></span>
                                  Why This Fits
                                </h4>
                                <p className="text-sm text-text-body dark:text-dark-text-secondary leading-relaxed">
                                  {job.whyFit}
                                </p>
                              </div>
                            )}

                            {/* Missing Skills */}
                            {job.missingSkill && (
                              <div>
                                <h4 className="text-sm font-semibold text-status-warning dark:text-status-warning mb-2 flex items-center gap-2">
                                  <span className="w-2 h-2 rounded-full bg-status-warning"></span>
                                  Skill Gap / Development Area
                                </h4>
                                <p className="text-sm text-text-body dark:text-dark-text-secondary leading-relaxed">
                                  {job.missingSkill}
                                </p>
                              </div>
                            )}

                            {/* Job Details */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2 border-t border-gray-200 dark:border-dark-border">
                              {job.salary && (
                                <div>
                                  <h4 className="text-xs font-semibold text-text-muted dark:text-dark-text-secondary mb-1">Salary Range</h4>
                                  <p className="text-sm text-text-heading dark:text-dark-text-primary">{job.salary}</p>
                                </div>
                              )}
                              {job.jobType && (
                                <div>
                                  <h4 className="text-xs font-semibold text-text-muted dark:text-dark-text-secondary mb-1">Job Type</h4>
                                  <p className="text-sm text-text-heading dark:text-dark-text-primary">{job.jobType}</p>
                                </div>
                              )}
                            </div>

                            {/* Skills */}
                            {job.skills && job.skills.length > 0 && (
                              <div>
                                <h4 className="text-sm font-semibold text-text-heading dark:text-dark-text-primary mb-2">
                                  Required Skills
                                </h4>
                                <div className="flex flex-wrap gap-2">
                                  {job.skills.slice(0, 10).map((skill, idx) => (
                                    <span
                                      key={idx}
                                      className="px-3 py-1 bg-gray-100 dark:bg-dark-bg-card text-text-body dark:text-dark-text-secondary rounded-full text-xs"
                                    >
                                      {skill}
                                    </span>
                                  ))}
                                  {job.skills.length > 10 && (
                                    <span className="px-3 py-1 text-text-muted dark:text-dark-text-secondary text-xs">
                                      +{job.skills.length - 10} more
                                    </span>
                                  )}
                                </div>
                              </div>
                            )}

                            {/* Job Description Preview */}
                            {job.description && (
                              <div>
                                <h4 className="text-sm font-semibold text-text-heading dark:text-dark-text-primary mb-2">
                                  Job Description Preview
                                </h4>
                                <p className="text-sm text-text-body dark:text-dark-text-secondary line-clamp-4 leading-relaxed">
                                  {job.description}
                                </p>
                              </div>
                            )}

                            {/* Action Buttons */}
                            <div className="pt-4 border-t border-gray-200 dark:border-dark-border flex flex-wrap items-center gap-3">
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleTailorResume(job);
                                }}
                                className="btn-primary text-sm py-2.5 px-4 flex items-center gap-2 font-medium"
                                title="Generate tailored resume for this job"
                              >
                                <FileText className="w-4 h-4" />
                                Tailor Resume
                              </button>
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleViewDetails(job, e);
                                }}
                                className="btn-secondary btn-secondary-dark text-sm py-2.5 px-4 flex items-center gap-2"
                                title="View full job details"
                              >
                                <Eye className="w-4 h-4" />
                                View Complete Details
                              </button>
                              {job.jobUrl && (
                                <a
                                  href={job.jobUrl}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="btn-secondary btn-secondary-dark text-sm py-2.5 px-4 flex items-center gap-2"
                                  onClick={(e) => e.stopPropagation()}
                                >
                                  <ExternalLink className="w-4 h-4" />
                                  View on Job Board
                                </a>
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

      {/* Job Details Modal */}
      {selectedJob && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50" onClick={() => setSelectedJob(null)}>
          <div className="bg-bg-card dark:bg-dark-bg-card rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="sticky top-0 bg-bg-card dark:bg-dark-bg-card border-b border-gray-200 dark:border-dark-border p-6 flex items-center justify-between">
              <h2 className="text-2xl font-bold text-text-heading dark:text-dark-text-primary">
                {selectedJob.jobTitle}
              </h2>
              <button
                onClick={() => setSelectedJob(null)}
                className="p-2 hover:bg-gray-100 dark:hover:bg-dark-bg-main rounded-lg transition-colors"
                aria-label="Close"
              >
                <X className="w-6 h-6 text-text-muted dark:text-dark-text-secondary" />
              </button>
            </div>
            
            <div className="p-6 space-y-6">
              {/* Basic Info */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h3 className="text-sm font-semibold text-text-muted dark:text-dark-text-secondary mb-1">Company</h3>
                  <p className="text-text-heading dark:text-dark-text-primary">{selectedJob.company}</p>
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-text-muted dark:text-dark-text-secondary mb-1">Location</h3>
                  <p className="text-text-heading dark:text-dark-text-primary">{selectedJob.location}</p>
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-text-muted dark:text-dark-text-secondary mb-1">Match Score</h3>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 bg-gray-200 dark:bg-dark-bg-main rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${getScoreColor(selectedJob.matchScore)}`}
                        style={{ width: `${selectedJob.matchScore}%` }}
                      />
                    </div>
                    <span className="text-sm font-semibold text-text-heading dark:text-dark-text-primary">
                      {selectedJob.matchScore}%
                    </span>
                  </div>
                </div>
                {selectedJob.salary && (
                  <div>
                    <h3 className="text-sm font-semibold text-text-muted dark:text-dark-text-secondary mb-1">Salary</h3>
                    <p className="text-text-heading dark:text-dark-text-primary">{selectedJob.salary}</p>
                  </div>
                )}
              </div>

              {/* Why This Fits */}
              {selectedJob.whyFit && (
                <div>
                  <h3 className="text-lg font-semibold text-text-heading dark:text-dark-text-primary mb-2">
                    Why This Fits
                  </h3>
                  <p className="text-text-body dark:text-dark-text-secondary">{selectedJob.whyFit}</p>
                </div>
              )}

              {/* Missing Skills */}
              {selectedJob.missingSkill && (
                <div>
                  <h3 className="text-lg font-semibold text-status-warning dark:text-status-warning mb-2">
                    Skill Gap
                  </h3>
                  <p className="text-text-body dark:text-dark-text-secondary">{selectedJob.missingSkill}</p>
                </div>
              )}

              {/* Job Description */}
              {selectedJob.description && (
                <div>
                  <h3 className="text-lg font-semibold text-text-heading dark:text-dark-text-primary mb-2">
                    Job Description
                  </h3>
                  <div className="text-text-body dark:text-dark-text-secondary whitespace-pre-wrap">
                    {selectedJob.description}
                  </div>
                </div>
              )}

              {/* Skills */}
              {selectedJob.skills && selectedJob.skills.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-text-heading dark:text-dark-text-primary mb-2">
                    Required Skills
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {selectedJob.skills.map((skill, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-gray-100 dark:bg-dark-bg-main text-text-body dark:text-dark-text-secondary rounded-full text-sm"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Actions */}
              <div className="flex items-center gap-4 pt-4 border-t border-gray-200 dark:border-dark-border">
                {selectedJob.jobUrl && (
                  <a
                    href={selectedJob.jobUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-primary text-sm py-2 px-4 flex items-center gap-2"
                  >
                    <ExternalLink className="w-4 h-4" />
                    View on Job Board
                  </a>
                )}
                <button
                  onClick={() => {
                    handleTailorResume(selectedJob);
                    setSelectedJob(null);
                  }}
                  className="btn-secondary btn-secondary-dark text-sm py-2 px-4 flex items-center gap-2"
                >
                  <FileText className="w-4 h-4" />
                  Generate Tailored Resume
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default JobMatchTable;
