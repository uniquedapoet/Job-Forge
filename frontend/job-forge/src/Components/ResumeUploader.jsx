import React, { useState, useContext } from "react";
import MainLayout from "./MainLayout";
import { UserContext } from "./UserContext";
import "../Icons+Styling/MainContent.css";

const ResumeUploader = ({ onLogout }) => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const { user } = useContext(UserContext); // Access the logged-in user from context

  const handleUpload = async () => {
    if (!file || !user?.id) {
      setMessage("Please select a file and ensure you are logged in.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", user.id); // Use the user ID from context

    try {
      const response = await fetch("http://127.0.0.1:5001/resumes/upload", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setMessage(response.ok ? `Success: ${data.message}` : `Error: ${data.error}`);
    } catch {
      setMessage("Error uploading the file.");
    }
  };

  return (
    <MainLayout onLogout={onLogout} title="Upload Resume">
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%" }}>
        <div className="main-content-card">
          <h2 className="main-content-heading">Upload Resume</h2>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
            style={{ marginBottom: "15px", width: "100%" }}
          />
          <button onClick={handleUpload} className="main-content-button">
            Upload
          </button>
          <p className="main-content-message">{message}</p>
        </div>
      </div>
    </MainLayout>
  );
};

export default ResumeUploader;