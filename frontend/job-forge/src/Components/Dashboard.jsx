import React, { useContext, useEffect, useState } from "react";
import MainLayout from "./MainLayout";
import "../Icons+Styling/MainContent.css";
import { UserContext } from "./UserContext";

const Dashboard = ({ onLogout }) => {
  const { savedJobs, user, setSavedJobs } = useContext(UserContext);
  const [scores, setScores] = useState({});
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [removingJobs, setRemovingJobs] = useState({}); // Track removing state per job

  // Log savedJobs 
  useEffect(() => {
    console.log("Updated savedJobs:", savedJobs);
  }, [savedJobs]);

  useEffect(() => {
    const fetchScores = async () => {
      const scoresData = {};
      setIsLoading(true);

      try {
        for (const job of savedJobs) {
          try {
            const response = await fetch("http://localhost:5001/resumes/resume_score", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                user_id: user.id,
                job_posting_id: job.job_id,
              }),
            });
        
            const data = await response.json();
        
            setScores(prev => ({
              ...prev,
              [job.job_id]: response.ok ? data.score : "N/A"
            }));
          } catch (error) {
            console.error("Error fetching score for job:", job.job_id, error);
            setScores(prev => ({
              ...prev,
              [job.job_id]: "N/A"
            }));
          }
        }
      } catch (err) {
        setError("Failed to load resume scores");
      } finally {
        setIsLoading(false);
      }
    };

    if (savedJobs.length > 0 && user) {
      fetchScores();
    } else {
      setScores({});
    }
  }, [savedJobs, user]);

  const handleRemoveJob = async (jobId) => {
    if (!user?.id) return;

    setRemovingJobs((prev) => ({ ...prev, [jobId]: true }));
    setError("");

    try {
      const response = await fetch(
        `http://localhost:5001/users/${user.id}/saved_jobs/${jobId}/delete`,
        { method: "POST" }
      );

      if (!response.ok) throw new Error("Failed to remove job");

      console.log("Before removing:", savedJobs);

      setSavedJobs((prevJobs) => {
        const updatedJobs = prevJobs.filter((job) => job.job_id !== jobId);
        console.log("After removing:", updatedJobs);
        return updatedJobs;
      });

      // Remove the score for the deleted job
      setScores((prev) => {
        const newScores = { ...prev };
        delete newScores[jobId];
        return newScores;
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setRemovingJobs((prev) => ({ ...prev, [jobId]: false }));
    }
  };

  return (
    <MainLayout onLogout={onLogout} title="Saved Jobs">
      <div className="job-search-container">
        {error && <p className="job-search-message" style={{ color: "red" }}>{error}</p>}

        <ul className="job-search-list">
          {savedJobs.length > 0 ? (
            savedJobs.map((job, index) => {
              const isProcessing = removingJobs[job.job_id] || false;
              const score = scores[job.job_id] !== undefined
                ? `${scores[job.job_id]}%`
                : isLoading
                  ? "Loading..."
                  : "N/A";

              return (
                <li key={index} className="job-search-item">
                  <div className="job-details">
                    <h3>{job.title}</h3>
                    <p>{job.company}</p>
                    <p>{job.location}</p>
                    <p><strong>Resume Score:</strong> {score}</p>
                    <button
                      onClick={() => handleRemoveJob(job.job_id)}
                      className="job-search-button"
                      style={{
                        backgroundColor: "#6c757d",
                        marginTop: "10px",
                      }}
                      disabled={isProcessing}
                    >
                      {isProcessing ? "Removing..." : "Remove"}
                    </button>
                  </div>
                </li>
              );
            })
          ) : (
            <h2 className="dashboard-title-message" style={{ textAlign: "center" }}>
              No saved jobs found.
            </h2>
          )}
        </ul>
      </div>
    </MainLayout>
  );
};

export default Dashboard;