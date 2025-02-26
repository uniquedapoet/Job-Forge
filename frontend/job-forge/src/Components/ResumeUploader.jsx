import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const ResumeUploader = () => {
  const [file, setFile] = useState(null);
  const [userId, setUserId] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUserIdChange = (event) => {
    setUserId(event.target.value);
  };

  const handleUpload = async () => {
    if (!file || !userId) {
      setMessage("Please select a file and enter a User ID.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", userId);

    try {
      const response = await fetch("http://127.0.0.1:5001/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setMessage(`Success: ${data.message}`);
      } else {
        setMessage(`Error: ${data.error}`);
      }
    } catch (error) {
      setMessage("Error uploading the file.");
    }
  };

  const handleBackToDashboard = () => {
    navigate("/dashboard");
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
      <div className="card" style={{ maxWidth: "600px", width: "100%", textAlign: "center" }}>
        <h2>Upload Resume</h2>
        <input
          type="text"
          placeholder="Enter User ID"
          value={userId}
          onChange={handleUserIdChange}
        />
        <br />
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        <br />
        <button onClick={handleUpload}>Upload Resume</button>
        <button onClick={handleBackToDashboard} style={{ marginLeft: "10px" }}>
          Back to Dashboard
        </button>
        <p className="message">{message}</p>
      </div>
    </div>
  );
};

export default ResumeUploader;