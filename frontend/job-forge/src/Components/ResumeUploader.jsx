import React, { useState } from "react";
import MainLayout from "./MainLayout";
import "../Icons+Styling/MainContent.css";

const ResumeUploader = ({ onLogout }) => {
  const [file, setFile] = useState(null);
  const [userId, setUserId] = useState("");
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!file || !userId) {
      setMessage("Please select a file and enter a User ID.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", userId);

    try {
      const response = await fetch("http://127.0.0.1:5001/upload", { method: "POST", body: formData });
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
            type="text"
            placeholder="Enter User ID"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            className="main-content-input"
          />
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