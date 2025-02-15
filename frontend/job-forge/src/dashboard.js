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
    <div>
      <h2>Welcome to the Dashboard</h2>
      <p>You have successfully logged in!</p>
      <button onClick={goToResumeUpload}>Upload Resume</button>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Dashboard;