import "./App.css";
import Auth from "./auth";
import ResumeUploader from "./resume_uploader";
import React, { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  
  return (
    <div>
      <h1>Flask + React Integration</h1>
      <p>Backend Response: {message}</p>
      <Auth />
      <ResumeUploader />
    </div>
  );
}

export default App;
