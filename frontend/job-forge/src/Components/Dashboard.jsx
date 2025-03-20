import React, { useContext, useEffect, useState } from "react";
import MainLayout from "./MainLayout";
import "../Icons+Styling/MainContent.css";
import { UserContext } from "./UserContext";

const Dashboard = ({ onLogout }) => {
  const { savedJobs, user, setSavedJobs, scores, setScores } = useContext(UserContext); // Get scores and setScores from UserContext

  // Fetch resume scores for all saved jobs that don't have a score yet
  useEffect(() => {
    const fetchScores = async () => {
      const scoresData = { ...scores }; // Start with existing scores
      for (const job of savedJobs) {
        try {
          const response = await fetch("http://localhost:5001/resume_score", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_id: user.id, // Assuming user._id is the user's ID
              job_posting_id: job.id, // Assuming job.id is the job posting ID
            }),
          });

          const data = await response.json();
          if (response.ok) {
            scoresData[job.id] = data.score; // Store the score for this job
          } else {
            console.error("Failed to fetch score for job:", job.id, data.error);
            scoresData[job.id] = "N/A"; // Use "N/A" if the score cannot be fetched
          }
        } catch (error) {
          console.error("Error fetching score for job:", job.id, error);
          scoresData[job.id] = "N/A"; // Use "N/A" if an error occurs
        }
      }
      setScores(scoresData); // Update the scores state
    };

    if (savedJobs.length > 0 && user) {
      fetchScores();
    }
  }, [savedJobs, user]); // Only run when savedJobs or user changes

  // Function to handle unsaving a job
  const handleUnsaveJob = (jobId) => {
    const updatedSavedJobs = savedJobs.filter((job) => job.id !== jobId);
    setSavedJobs(updatedSavedJobs); // Update the savedJobs list in the context
  };

  return (
    <MainLayout onLogout={onLogout} title="Saved Jobs">
      <div className="job-search-container">
        <ul className="job-search-list">
          {savedJobs.length > 0 ? (
            savedJobs.map((job, index) => (
              <li key={index} className="job-search-item">
                <div className="job-details">
                  <h3>{job.title}</h3>
                  <p>{job.company}</p>
                  <p>{job.location}</p>
                  <p>
                    <strong>Resume Score:</strong> {scores[job.id] || "Loading..."}
                  </p>
                  <button
                    onClick={() => handleUnsaveJob(job.id)}
                    className="job-search-button"
                    style={{
                      backgroundColor: "#ba5624",
                      marginTop: "10px",
                    }}
                  >
                    Unsave
                  </button>
                </div>
              </li>
            ))
          ) : (
            <h2 className="dashboard-title-message">No saved jobs found.</h2>
          )}
        </ul>
      </div>
    </MainLayout>
  );
};

export default Dashboard;