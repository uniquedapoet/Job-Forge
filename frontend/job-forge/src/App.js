import "./App.css";
import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Auth from "./auth";
import Dashboard from "./dashboard";
import ResumeUploader from "./resume_uploader";

function App() {
  return (
    <Router>
      <div>
        <h1>Flask + React Integration</h1>
        <Routes>
          <Route path="/" element={<Auth />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/upload-resume" element={<ResumeUploader />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;