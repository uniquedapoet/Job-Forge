import React, { useState, useEffect, useContext, useCallback } from "react";
import MainLayout from "./MainLayout";
import "../Icons+Styling/MainContent.css";
import { UserContext } from "./UserContext";

const JobSearch = ({ onLogout }) => {
  const [jobTitle, setJobTitle] = useState("");
  const [location, setLocation] = useState("");
  const [jobs, setJobs] = useState(null);
  const [error, setError] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [savingJobs, setSavingJobs] = useState({});

  const { user, savedJobs, setSavedJobs } = useContext(UserContext);

  const fetchSavedJobs = useCallback(async () => {
    if (!user?.id) {
      setSavedJobs([]);
      return;
    }
    
    try {
      const response = await fetch(`http://localhost:5001/users/${user.id}/saved_jobs`);
      if (!response.ok) return;
      
      const data = await response.json();
      setSavedJobs(data || []);
    } catch (err) {
      console.error("Error fetching saved jobs:", err);
    }
  }, [user?.id, setSavedJobs]);

  useEffect(() => {
    if (user) {
      setLocation(user.city || "");
      setSuggestions(user.job_titles ? user.job_titles.split(",").map(title => title.trim()) : []);
      fetchSavedJobs();
    } else {
      setSavedJobs([]);
    }
  }, [user, fetchSavedJobs, setSavedJobs]);

  const handleSearch = async () => {
    if (!jobTitle.trim()) {
      setError("Please enter a job title");
      return;
    }

    setError("");
    setIsSearching(true);

    try {
      const response = await fetch("http://localhost:5001/jobs/job_search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_title: jobTitle, location }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Failed to search for jobs");

      setJobs(data.jobs || []);
    } catch (err) {
      setError(err.message);
      setJobs([]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleSaveJob = async (job) => {
    if (!user?.id || !job.id) {
      setError("You need to be logged in to save jobs");
      return;
    }
    
    setSavingJobs(prev => ({ ...prev, [job.id]: true }));
    setError("");
    const isSaved = savedJobs.some(savedJob => savedJob.job_id === job.id);
    
    try {
      if (isSaved) {
        const response = await fetch(
          `http://localhost:5001/users/${user.id}/saved_jobs/${job.id}/delete`,
          { method: "POST" }
        );
        
        if (!response.ok) throw new Error("Failed to unsave job");
        
        setSavedJobs(savedJobs.filter(savedJob => savedJob.job_id !== job.id));
      } else {
        const jobData = {
          job_id: job.id,
          title: job.title,
          company: job.company,
          location: job.location,
          user_id: user.id
        };

        const response = await fetch(
          `http://localhost:5001/users/${user.id}/saved_jobs/${job.id}/save`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(jobData),
          }
        );
        
        if (!response.ok) throw new Error("Failed to save job");
        
        setSavedJobs([...savedJobs, jobData]);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setSavingJobs(prev => ({ ...prev, [job.id]: false }));
    }
  };

  return (
    <MainLayout onLogout={onLogout} title="Job Search">
      <div className="job-search-container">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSearch();
          }}
          className="job-search-header"
        >
          <input
            type="text"
            placeholder="Job Title"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            list="job-suggestions"
            className="job-search-input"
          />
          <datalist id="job-suggestions">
            {suggestions.map((title, index) => (
              <option key={index} value={title} />
            ))}
          </datalist>
          <input
            type="text"
            placeholder="Location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="job-search-input"
          />
          <button 
            type="submit" 
            className="job-search-button"
            disabled={isSearching}
          >
            {isSearching ? "Searching..." : "Search"}
          </button>
        </form>
        
        {error && <p className="job-search-message" style={{ color: "red" }}>{error}</p>}
        
        {jobs !== null && (
          <ul className="job-search-list">
            {jobs.length > 0 ? (
              jobs.map((job, index) => {
                const isSaved = savedJobs.some(savedJob => savedJob.job_id === job.id);
                const isProcessing = savingJobs[job.id] || false;
                
                return (
                  <li key={index} className="job-search-item">
                    <div className="job-details">
                      <h3>{job.title}</h3>
                      <p>{job.company}</p>
                      <p>{job.location}</p>
                      <button
                        onClick={() => handleSaveJob(job)}
                        className="job-search-button"
                        style={{
                          backgroundColor: isSaved ? "#6c757d" : "#ba5624",
                          marginTop: "10px",
                        }}
                        disabled={isProcessing}
                      >
                        {isProcessing ? "Processing..." : (isSaved ? "Remove" : "Save")}
                      </button>
                    </div>
                  </li>
                );
              })
            ) : (
              <p className="job-search-message">No jobs found</p>
            )}
          </ul>
        )}
      </div>
    </MainLayout>
  );
};

export default JobSearch;