import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import JobSearch from "./JobSearch";

const Dashboard = () => {
  const navigate = useNavigate();
  const [allJobs, setAllJobs] = useState([]); // Stores all jobs fetched from the backend
  const [filteredJobs, setFilteredJobs] = useState([]); // Stores jobs filtered by user input
  const [isSearching, setIsSearching] = useState(false); // Tracks whether a search is in progress

  // Fetch all jobs when the component mounts
  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch("/jobs");
        const data = await response.json();
        setAllJobs(data.jobs); // Store all jobs
        setFilteredJobs(data.jobs); // Initially, display all jobs
      } catch (error) {
        console.error("Error fetching jobs:", error);
      }
    };

    fetchJobs();
  }, []);

  const handleLogout = () => {
    navigate("/");
  };

  const goToResumeUpload = () => {
    navigate("/upload-resume");
  };

  // Filter jobs based on job title and location
  const handleSearch = (jobTitle, location) => {
    setIsSearching(true); // Indicate that a search is in progress

    const filtered = allJobs.filter((job) => {
      const matchesTitle = job.title.toLowerCase().includes(jobTitle.toLowerCase());
      const matchesLocation = job.location.toLowerCase().includes(location.toLowerCase());
      return matchesTitle && matchesLocation;
    });

    setFilteredJobs(filtered); // Update the filtered jobs
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "80vh",
        flexDirection: "column",
      }}
    >
      <div className="card" style={{ maxWidth: "800px", width: "100%", textAlign: "center" }}>
        <h2>Welcome to Job Forge</h2>
        <p>You have successfully logged in!</p>

        {/* Add the JobSearch component */}
        <JobSearch onSearch={handleSearch} />

        {/* Display the filtered jobs or a message if no jobs match */}
        <div>
          {isSearching && filteredJobs.length === 0 ? (
            <p>No jobs match your search criteria.</p>
          ) : (
            filteredJobs.map((job, index) => (
              <div key={index} style={{ margin: "10px", padding: "10px", border: "1px solid #ccc" }}>
                <h3>{job.title}</h3>
                <p>{job.company}</p>
                <p>{job.location}</p>
                <p>{job.description}</p>
              </div>
            ))
          )}
        </div>

        <button onClick={goToResumeUpload}>Upload Resume</button>
        <button onClick={handleLogout} style={{ marginLeft: "10px" }}>
          Logout
        </button>
      </div>
    </div>
  );
};

export default Dashboard;