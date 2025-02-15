import React from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    navigate("/");
  };

  const goToResumeUpload = () => {
    navigate("/upload-resume");
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
        <button onClick={goToResumeUpload}>Upload Resume</button>
        <button onClick={handleLogout} style={{ marginLeft: "10px" }}>
          Logout
        </button>
      </div>
    </div>
  );
};

export default Dashboard;