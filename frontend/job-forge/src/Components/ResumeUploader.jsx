import React, { useState, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import MainLayout from "./MainLayout";
import { UserContext } from "./UserContext";
import "../Icons+Styling/MainContent.css";

const ResumeUploader = ({ onLogout }) => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState({ text: "", isError: false });
  const { user } = useContext(UserContext);
  const [hasResume, setHasResume] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const checkExistingResume = async () => {
      if (user?.id) {
        try {
          const response = await fetch(`http://localhost:5001/resumes/view/${user.id}`);
          if (response.ok) {
            setHasResume(true);
          }
        } catch (error) {
          console.error("Error checking resume:", error);
        }
      }
    };
    checkExistingResume();
  }, [user]);

  const handleUpload = async () => {
    if (!file || !user?.id) {
      setMessage({ text: "Please select a file and ensure you are logged in.", isError: true });
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", user.id);

    try {
      const response = await fetch("http://localhost:5001/resumes/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setMessage({ text: data.message || "Resume uploaded successfully", isError: false });
        setHasResume(true);
      } else {
        setMessage({ text: data.error || "Error uploading resume", isError: true });
      }
    } catch (error) {
      setMessage({ text: "Error uploading the file.", isError: true });
    }
  };

  const handleEditResume = () => {
    if (user?.id) {
      navigate(`/edit-resume`);
    }
  };

  const handleDownloadResume = async () => {
    if (user?.id) {
      try {
        const response = await fetch(`http://localhost:5001/resumes/download/${user.id}`);
        if (response.ok) {
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = `resume_${user.id}.pdf`;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
        } else {
          const error = await response.json();
          setMessage({ text: error.error || "Failed to download resume", isError: true });
        }
      } catch (error) {
        setMessage({ text: "Error downloading resume", isError: true });
      }
    }
  };

  return (
    <MainLayout onLogout={onLogout} title="Resume Manager">
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%" }}>
        <div className="main-content-card">
          <h2 className="main-content-heading">Resume Manager</h2>

          {/* Upload Section */}
          <div style={{ marginBottom: "20px" }}>
            <h3>{hasResume ? "Replace Resume" : "Upload Resume"}</h3>
            <input
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={(e) => setFile(e.target.files[0])}
              style={{ marginBottom: "15px", width: "100%" }}
            />
            <button onClick={handleUpload} className="main-content-button">
              {hasResume ? "Replace Resume" : "Upload Resume"}
            </button>
          </div>

          {/* Resume Actions */}
          {hasResume && (
            <div style={{ marginTop: "20px" }}>
              <h3>Resume Actions</h3>
              <button 
                onClick={handleEditResume} 
                className="main-content-button"
                style={{ marginRight: "10px" }}
              >
                Edit Resume
              </button>
              <button 
                onClick={handleDownloadResume} 
                className="main-content-button"
              >
                Download Resume
              </button>
            </div>
          )}

          {/* Status Message */}
          <p 
            className="main-content-message" 
            style={{ color: message.isError ? "red" : "green", marginTop: "15px" }}
          >
            {message.text}
          </p>

          {/* Current Resume Status */}
          <p style={{ marginTop: "10px", fontStyle: "italic" }}>
            {hasResume ? "You have a resume on file." : "No resume uploaded yet."}
          </p>
        </div>
      </div>
    </MainLayout>
  );
};

export default ResumeUploader;
