import React, { useContext, useEffect, useState } from "react";
import MainLayout from "./MainLayout";
import "../Icons+Styling/MainContent.css";
import { UserContext } from "./UserContext";

const Dashboard = ({ onLogout }) => {
  const { user } = useContext(UserContext);
  const [savedJobs, setSavedJobs] = useState([]);
  const [jobDetails, setJobDetails] = useState({});
  const [scores, setScores] = useState({});
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [removingJobs, setRemovingJobs] = useState({});
  const [loadingJobs, setLoadingJobs] = useState(true);

  const fetchJobDetails = async (jobId) => {
    try {
      const response = await fetch(`http://localhost:5001/jobs/${jobId}`);
      if (!response.ok) throw new Error("Failed to fetch job details");
      
      const data = await response.json();
      const job = data.jobs || data.job || data;
      
      if (!job) throw new Error("No job data received");

      return {
        id: job.id || job.job_id,
        title: job.title,
        company: job.company,
        location: job.location,
      };
    } catch (err) {
      console.error(`Error fetching details for job ${jobId}:`, err);
      return null;
    }
  };

  const fetchSavedJobs = async () => {
    if (!user?.id) {
      setSavedJobs([]);
      setLoadingJobs(false);
      return;
    }

    setLoadingJobs(true);
    setError("");

    try {
      const savedResponse = await fetch(`http://localhost:5001/users/${user.id}/saved_jobs`);
      const savedJobsData = await savedResponse.json();

      if (!savedResponse.ok || !Array.isArray(savedJobsData)) {
        console.warn("Saved jobs fetch failed or returned unexpected format:", savedJobsData);
        setSavedJobs([]);
        setJobDetails({});
        return;
      }

      if (savedJobsData.length === 0) {
        setSavedJobs([]);
        setJobDetails({});
        return;
      }

      setSavedJobs(savedJobsData);

      const detailsPromises = savedJobsData.map(job => fetchJobDetails(job.job_id));
      const detailsResults = await Promise.all(detailsPromises);

      const detailsMap = {};
      savedJobsData.forEach((savedJob, index) => {
        if (detailsResults[index]) {
          detailsMap[savedJob.job_id] = detailsResults[index];
        }
      });

      setJobDetails(detailsMap);
    } catch (err) {
      console.error("Unexpected fetch error:", err);
      setError("");
      setSavedJobs([]);
    } finally {
      setLoadingJobs(false);
    }
  };

  const fetchScores = async () => {
    if (!savedJobs.length || !user) return;

    setIsLoading(true);
    setError("");

    try {
      const scoresData = {};
      
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
          scoresData[job.job_id] = response.ok ? data.score : "N/A";
        } catch (error) {
          console.error("Error fetching score for job:", job.job_id, error);
          scoresData[job.job_id] = "N/A";
        }
      }

      setScores(scoresData);
    } catch (err) {
      setError("Failed to load resume scores");
    } finally {
      setIsLoading(false);
    }
  };

  const handleRemoveJob = async (jobId) => {
    if (!user?.id) return;

    setRemovingJobs(prev => ({ ...prev, [jobId]: true }));
    setError("");

    try {
      const response = await fetch(
        `http://localhost:5001/users/${user.id}/saved_jobs/${jobId}/delete`,
        { method: "POST" }
      );

      if (!response.ok) throw new Error("Failed to remove job");

      await fetchSavedJobs();

      setScores(prev => {
        const newScores = { ...prev };
        delete newScores[jobId];
        return newScores;
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setRemovingJobs(prev => ({ ...prev, [jobId]: false }));
    }
  };

  useEffect(() => {
    fetchSavedJobs();
  }, [user]);

  useEffect(() => {
    fetchScores();
  }, [savedJobs]);

  return (
    <MainLayout onLogout={onLogout} title="Saved Jobs">
      <div className="job-search-container">
        {error && (
          <p className="job-search-message" style={{ color: "red" }}>
            {error}
          </p>
        )}

        {loadingJobs ? (
          <p className="job-search-message">Loading saved jobs...</p>
        ) : (
          <ul className="job-search-list">
            {savedJobs.length > 0 ? (
              savedJobs.map((savedJob, index) => {
                const job = jobDetails[savedJob.job_id];
                const isProcessing = removingJobs[savedJob.job_id] || false;
                const score = scores[savedJob.job_id] !== undefined
                  ? `${scores[savedJob.job_id]}%`
                  : isLoading
                    ? "Loading..."
                    : "N/A";

                if (!job) {
                  return (
                    <li key={index} className="job-search-item">
                      <div className="job-details">
                        <p>Loading job details for ID: {savedJob.job_id}...</p>
                      </div>
                    </li>
                  );
                }

                return (
                  <li key={index} className="job-search-item">
                    <div className="job-details">
                      <h3>{job.title}</h3>
                      <p>{job.company}</p>
                      <p>{job.location}</p>
                      <p><strong>Resume Score:</strong> {score}</p>
                      <button
                        onClick={() => handleRemoveJob(savedJob.job_id)}
                        className="job-search-button"
                        style={{ backgroundColor: "#6c757d", marginTop: "10px" }}
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
                {user ? "No saved jobs found" : "Please log in to view saved jobs"}
              </h2>
            )}
          </ul>
        )}
      </div>
    </MainLayout>
  );
};

export default Dashboard;
