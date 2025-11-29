import React, { useState, useEffect } from 'react';
import { Upload, X, Menu, CheckCircle } from 'lucide-react';
import Logo from './Logo';
import { useFileUpload } from '../hooks/useFileUpload';
import { useLocalStorage } from '../hooks/useLocalStorage';
import LoadingSpinner from './LoadingSpinner';

const Sidebar = ({ isOpen, onClose, isMobile, onFileUploaded, onFetchJobs, onAnalyze, toast }) => {
  const [targetIndustries, setTargetIndustries] = useLocalStorage('careerlens_industries', ['FinTech']);
  const [minSalary, setMinSalary] = useLocalStorage('careerlens_min_salary', 4000);
  const [maxSalary, setMaxSalary] = useLocalStorage('careerlens_max_salary', 90000);
  const [uploadedFileName, setUploadedFileName] = useState(null);
  
  // Job fetch inputs
  const [jobKeywords, setJobKeywords] = useLocalStorage('careerlens_job_keywords', '');
  const [jobLocation, setJobLocation] = useLocalStorage('careerlens_job_location', 'Hong Kong');
  const [jobType, setJobType] = useLocalStorage('careerlens_job_type', 'fulltime');
  const [numJobs, setNumJobs] = useLocalStorage('careerlens_num_jobs', 25);

  const { uploadFile, uploading, progress, uploadedFile, reset } = useFileUpload(
    (fileResult, profile) => {
      setUploadedFileName(fileResult.filename || fileResult.name);
      toast?.success('Resume uploaded successfully!');
      onFileUploaded?.(fileResult, profile);
    },
    (error) => {
      toast?.error(error);
    }
  );

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      uploadFile(file);
    }
  };

  const handleRemoveFile = () => {
    reset();
    setUploadedFileName(null);
    toast?.info('Resume removed');
  };

  const removeIndustry = (industry) => {
    setTargetIndustries(targetIndustries.filter(i => i !== industry));
  };

  const addIndustry = (e) => {
    if (e.key === 'Enter' && e.target.value.trim()) {
      setTargetIndustries([...targetIndustries, e.target.value.trim()]);
      e.target.value = '';
    }
  };

  const sidebarContent = (
    <div className="h-full flex flex-col bg-bg-sidebar text-white">
      {/* Header with Logo */}
      <div className="p-6 border-b border-navy-light">
        <div className="flex items-center justify-between">
          <div className="text-white">
            <Logo variant="full" size="default" darkMode={true} />
          </div>
          {isMobile && (
            <button
              onClick={onClose}
              className="p-2 hover:bg-navy-light rounded-lg transition-colors"
              aria-label="Close sidebar"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>

      {/* Scrollable Content */}
      <div className="flex-1 overflow-y-auto scrollbar-thin p-6 space-y-6">
        {/* Upload Section */}
        <div>
          <h3 className="text-sm font-semibold text-gray-300 mb-3 uppercase tracking-wide">
            Upload Resume
          </h3>
          {uploadedFileName ? (
            <div className="border-2 border-accent rounded-lg p-4 bg-accent/10">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2 flex-1 min-w-0">
                  <CheckCircle className="w-5 h-5 text-status-success flex-shrink-0" />
                  <span className="text-sm text-white truncate">{uploadedFileName}</span>
                </div>
                <button
                  onClick={handleRemoveFile}
                  className="p-1 hover:bg-navy-light rounded transition-colors flex-shrink-0"
                  aria-label="Remove file"
                >
                  <X className="w-4 h-4 text-gray-400" />
                </button>
              </div>
              {progress > 0 && progress < 100 && (
                <div className="w-full bg-navy-light rounded-full h-1.5 mt-2">
                  <div
                    className="bg-accent h-1.5 rounded-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              )}
            </div>
          ) : (
            <label className="block">
              <input
                type="file"
                accept=".pdf,.docx"
                onChange={handleFileUpload}
                disabled={uploading}
                className="hidden"
              />
              <div className={`border-2 border-dashed border-navy-light rounded-lg p-6 text-center cursor-pointer hover:border-accent transition-colors group ${
                uploading ? 'opacity-50 cursor-not-allowed' : ''
              }`}>
                {uploading ? (
                  <>
                    <LoadingSpinner size="lg" className="mx-auto mb-2" />
                    <p className="text-sm text-gray-300 mb-1">Uploading...</p>
                    <p className="text-xs text-gray-400">{progress}%</p>
                  </>
                ) : (
                  <>
                    <Upload className="w-8 h-8 mx-auto mb-2 text-gray-400 group-hover:text-accent transition-colors" />
                    <p className="text-sm text-gray-300 mb-1">PDF or DOCX</p>
                    <p className="text-xs text-gray-400">Click to upload or drag and drop</p>
                  </>
                )}
              </div>
            </label>
          )}
        </div>

        {/* Filters Section */}
        <div className="space-y-6">
          {/* Target Industries */}
          <div>
            <label className="block text-sm font-semibold text-gray-300 mb-3 uppercase tracking-wide">
              Target Industries
            </label>
            <div className="space-y-2">
              <input
                type="text"
                placeholder="Type and press Enter..."
                onKeyPress={addIndustry}
                className="w-full px-4 py-2 bg-navy-light border border-navy rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-accent"
              />
              <div className="flex flex-wrap gap-2 mt-2">
                {targetIndustries.map((industry, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center gap-1 px-3 py-1 bg-accent text-white rounded-full text-sm"
                  >
                    {industry}
                    <button
                      onClick={() => removeIndustry(industry)}
                      className="hover:text-gray-200"
                      aria-label={`Remove ${industry}`}
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Salary Range */}
          <div>
            <label className="block text-sm font-semibold text-gray-300 mb-3 uppercase tracking-wide">
              Min. Salary (HK$)
            </label>
            <div className="space-y-3">
              <div className="flex justify-between text-sm text-white mb-2 font-medium">
                <span>HK${(minSalary / 1000).toFixed(0)}k</span>
                <span className="text-gray-400">Max: HK${(maxSalary / 1000).toFixed(0)}k</span>
              </div>
              <div className="relative">
                <input
                  type="range"
                  min="4000"
                  max="90000"
                  step="1000"
                  value={minSalary}
                  onChange={(e) => {
                    const newMin = Number(e.target.value);
                    if (newMin <= maxSalary) {
                      setMinSalary(newMin);
                    }
                  }}
                  className="w-full h-2 bg-navy-light rounded-lg appearance-none cursor-pointer accent-accent"
                  style={{
                    background: `linear-gradient(to right, #3B82F6 0%, #3B82F6 ${((minSalary - 4000) / (90000 - 4000)) * 100}%, #2C3E50 ${((minSalary - 4000) / (90000 - 4000)) * 100}%, #2C3E50 100%)`
                  }}
                />
              </div>
              <div className="flex justify-between text-xs text-gray-400">
                <span>HK$4k</span>
                <span>HK$90k</span>
              </div>
            </div>
          </div>

          {/* Job Fetch Inputs */}
          <div className="space-y-4 pt-4 border-t border-navy-light">
            <h3 className="text-sm font-semibold text-gray-300 mb-3 uppercase tracking-wide">
              Job Search Parameters
            </h3>
            
            {/* Keywords */}
            <div>
              <label className="block text-xs text-gray-400 mb-2">
                Keywords
              </label>
              <input
                type="text"
                value={jobKeywords}
                onChange={(e) => setJobKeywords(e.target.value)}
                placeholder="e.g., Software Engineer, Product Manager"
                className="w-full px-4 py-2 bg-navy-light border border-navy rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-accent"
              />
            </div>

            {/* Location */}
            <div>
              <label className="block text-xs text-gray-400 mb-2">
                Location
              </label>
              <input
                type="text"
                value={jobLocation}
                onChange={(e) => setJobLocation(e.target.value)}
                placeholder="Hong Kong"
                className="w-full px-4 py-2 bg-navy-light border border-navy rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-accent"
              />
            </div>

            {/* Job Type */}
            <div>
              <label className="block text-xs text-gray-400 mb-2">
                Job Type
              </label>
              <select
                value={jobType}
                onChange={(e) => setJobType(e.target.value)}
                className="w-full px-4 py-2 bg-navy-light border border-navy rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-accent"
              >
                <option value="fulltime">Full-time</option>
                <option value="parttime">Part-time</option>
                <option value="contract">Contract</option>
                <option value="internship">Internship</option>
              </select>
            </div>

            {/* Number of Jobs */}
            <div>
              <label className="block text-xs text-gray-400 mb-2">
                Number of Jobs to Fetch
              </label>
              <input
                type="number"
                min="5"
                max="50"
                value={numJobs}
                onChange={(e) => setNumJobs(Math.max(5, Math.min(50, Number(e.target.value))))}
                className="w-full px-4 py-2 bg-navy-light border border-navy rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-accent"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="p-6 border-t border-navy-light space-y-3">
        {/* Step 1: Fetch Market Jobs */}
        <button
          onClick={() => {
            if (!uploadedFileName) {
              toast?.warning('Please upload a resume first');
              return;
            }
            onFetchJobs?.({
              keywords: jobKeywords,
              location: jobLocation,
              jobType: jobType,
              numJobs: numJobs,
              industries: targetIndustries,
              minSalary,
              maxSalary,
            });
          }}
          disabled={uploading || !uploadedFileName}
          className={`w-full bg-accent hover:bg-accent-dark text-white font-semibold py-3 px-4 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 ${
            uploading || !uploadedFileName ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {uploading ? (
            <span className="flex items-center justify-center gap-2">
              <LoadingSpinner size="sm" />
              Uploading...
            </span>
          ) : (
            'Fetch Market Jobs'
          )}
        </button>

        {/* Step 2: Analyze and Rank */}
        <button
          onClick={() => {
            if (!uploadedFileName) {
              toast?.warning('Please upload a resume first');
              return;
            }
            onAnalyze?.({
              industries: targetIndustries,
              minSalary,
              maxSalary,
            });
          }}
          disabled={uploading || !uploadedFileName}
          className={`w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-4 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 ${
            uploading || !uploadedFileName ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          Analyze and Rank Top 15 Matches
        </button>
      </div>
    </div>
  );

  if (isMobile) {
    return (
      <>
        {/* Mobile Overlay */}
        {isOpen && (
          <div
            className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
            onClick={onClose}
          />
        )}
        {/* Mobile Sidebar */}
        <div
          className={`fixed top-0 left-0 h-full w-64 z-50 transform transition-transform duration-300 ease-in-out lg:hidden ${
            isOpen ? 'translate-x-0' : '-translate-x-full'
          }`}
        >
          {sidebarContent}
        </div>
      </>
    );
  }

  // Desktop Sidebar
  return (
    <aside className="hidden lg:flex lg:w-64 lg:flex-shrink-0">
      {sidebarContent}
    </aside>
  );
};

export default Sidebar;
