import React, { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import JobSearch from "./JobSearch";
import { UserContext } from "./UserContext"; // Import the UserContext

const Dashboard = () => {
  const navigate = useNavigate();
  const [allJobs, setAllJobs] = useState([]); // Storing jobs fetched
  const [filteredJobs, setFilteredJobs] = useState([]); // Storing jobs filtered by user input
  const [isSearching, setIsSearching] = useState(false); // Tracks whether a search is in progress
  const { user } = useContext(UserContext); // Access user from context

  // Fetch all jobs when the component mounts
  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch("/jobs");
        const data = await response.json();
        setAllJobs(data.jobs);
        setFilteredJobs(data.jobs);
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
    setIsSearching(true);

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
        {/* Display the user's name */}
        {user && (
          <p>Welcome back, {user.first_name} {user.last_name}!</p>
        )}

        <JobSearch onSearch={handleSearch} />

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