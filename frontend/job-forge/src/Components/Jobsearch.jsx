import React, { useState, useEffect } from "react";
import MainLayout from "./MainLayout";
import "../Icons+Styling/MainContent.css";

const JobSearch = ({ onLogout, user }) => {
  const [jobTitle, setJobTitle] = useState("");
  const [location, setLocation] = useState("");
  const [jobs, setJobs] = useState([]);
  const [error, setError] = useState("");
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    if (user) {
      setLocation(user.city || ""); 
      setSuggestions(user.job_titles ? user.job_titles.split(",").map(title => title.trim()) : []);
    }
  }, [user]);

  const handleSearch = async () => {
    setError("");

    try {
      const response = await fetch("http://localhost:5001/job_search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_title: jobTitle, location }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Something went wrong");

      setJobs(data.jobs);
    } catch (err) {
      setError(err.message);
      setJobs([]);
    }
  };

  return (
    <MainLayout onLogout={onLogout} title="Job Search">
      <div className="job-search-container">
        <div className="job-search-header">
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
          <button onClick={handleSearch} className="job-search-button">
            Search
          </button>
        </div>
        {error && <p className="job-search-message" style={{ color: "red" }}>{error}</p>}
        <ul className="job-search-list">
          {jobs.map((job, index) => (
            <li key={index}>
              {job.title} - {job.company} ({job.location})
            </li>
          ))}
        </ul>
      </div>
    </MainLayout>
  );
};

export default JobSearch;
