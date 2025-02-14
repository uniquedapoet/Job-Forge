import React, { useState } from "react";

const ResumeUploader = () => {
    const [file, setFile] = useState(null);
    const [userId, setUserId] = useState("");
    const [message, setMessage] = useState("");

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

    return (
        <div style={{ padding: "20px", textAlign: "center" }}>
            <h2>Upload Resume</h2>
            <input
                type="text"
                placeholder="Enter User ID"
                value={userId}
                onChange={handleUserIdChange}
                style={{ padding: "10px", marginBottom: "10px", width: "200px" }}
            />
            <br />
            <input type="file" accept=".pdf" onChange={handleFileChange} />
            <br />
            <button
                onClick={handleUpload}
                style={{
                    marginTop: "10px",
                    padding: "10px 20px",
                    cursor: "pointer",
                    backgroundColor: "#007bff",
                    color: "#fff",
                    border: "none",
                    borderRadius: "5px",
                }}
            >
                Upload Resume
            </button>
            <p style={{ marginTop: "10px", color: "red" }}>{message}</p>
        </div>
    );
};

export default ResumeUploader;
