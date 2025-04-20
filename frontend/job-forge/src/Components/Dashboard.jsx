import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import MainLayout from "./MainLayout";
import "../Icons+Styling/MainContent.css";
import { UserContext } from "./UserContext";
import JobModal from "./JobModal";

const Dashboard = ({ onLogout }) => {
  const { user } = useContext(UserContext);
  const [savedJobs, setSavedJobs] = useState([]);
  const [jobDetails, setJobDetails] = useState({});
  const [scores, setScores] = useState({});
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [removingJobs, setRemovingJobs] = useState({});
  const [loadingJobs, setLoadingJobs] = useState(true);
  const [selectedJob, setSelectedJob] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const navigate = useNavigate();

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
        job_type: job.job_type,
        date_posted: job.date_posted,
        description: job.description,
        job_url: job.job_url
      };
    } catch (err) {
      console.error(`Error fetching details for job ${jobId}:`, err);
      return null;
    }
  };

  const handleJobClick = async (job) => {
    try {
      const jobId = job.job_id || job.id;
      const response = await fetch(`http://localhost:5001/jobs/${jobId}`);
      if (!response.ok) throw new Error("Failed to fetch job details");
      
      const data = await response.json();
      const jobData = data.jobs || data.job || data;
      
      if (!jobData) throw new Error("No job data received");

      setSelectedJob({
        id: jobData.id || jobData.job_id,
        title: jobData.title,
        company: jobData.company,
        location: jobData.location,
        job_type: jobData.job_type,
        date_posted: jobData.date_posted,
        description: jobData.description,
        job_url: jobData.job_url
      });
      setShowModal(true);
    } catch (err) {
      setError(err.message);
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

        const uniqueJobs = Array.from(
          new Map(savedJobsData.map(job => [job.job_id, job])).values()
        );
        setSavedJobs(uniqueJobs);


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
      setError("Failed to load saved jobs");
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
      for (let i = 0; i < savedJobs.length; i++) {
        const job = savedJobs[i];
  
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
          const score = response.ok ? data.score : "N/A";
  
          // Update score for just this job
          setScores((prev) => ({
            ...prev,
            [job.job_id]: score,
          }));
        } catch (err) {
          console.error(`Error scoring job ${job.job_id}`, err);
          setScores((prev) => ({
            ...prev,
            [job.job_id]: "N/A",
          }));
        }
      }
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
                const job = jobDetails[savedJob.job_id] || savedJob;
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
                  <li 
                    key={index} 
                    className="job-search-item"
                    onClick={() => handleJobClick(job)}
                    style={{ cursor: "pointer" }}
                  >
                    <div className="job-details">
                      <h3>{job.title}</h3>
                      <p>{job.company}</p>
                      <p>{job.location}</p>
                      <p><strong>Resume Score:</strong> {score}</p>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleRemoveJob(savedJob.job_id);
                        }}
                        className="job-search-button"
                        style={{ backgroundColor: "#6c757d", marginTop: "10px" }}
                        disabled={isProcessing}
                      >
                        {isProcessing ? "Removing..." : "Remove"}
                      </button>
                      <button
                        className="job-search-button"
                        style={{ 
                          marginLeft: "10px",
                          backgroundColor:"#ba5624"
                        }}
                        onClick={() => navigate("/edit-resume")}
                      >
                        Get Suggestions
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

        {showModal && selectedJob && (
          <JobModal
            job={selectedJob}
            onClose={() => setShowModal(false)}
          />
        )}
      </div>
    </MainLayout>
  );
};

export default Dashboard;
