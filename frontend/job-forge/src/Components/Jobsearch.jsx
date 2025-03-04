import React, { useState } from "react";
import MainLayout from "./MainLayout";
import "../Icons+Styling/MainContent.css";

const JobSearch = ({ onLogout }) => {
  const [jobTitle, setJobTitle] = useState("");
  const [location, setLocation] = useState("");
  const [jobs, setJobs] = useState([]);
  const [error, setError] = useState("");

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
      <div>
        <input
          type="text"
          placeholder="Job Title"
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          className="main-content-input"
        />
        <input
          type="text"
          placeholder="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="main-content-input"
        />
        <button onClick={handleSearch} className="main-content-button">
          Search
        </button>
        {error && <p className="main-content-message" style={{ color: "red" }}>{error}</p>}
        <ul className="main-content-list">
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