import "./App.css";
import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation, useNavigate } from "react-router-dom";
import Auth from "./auth";
import Dashboard from "./dashboard";
import ResumeUploader from "./resume_uploader";
import logo from "./JF_LOGO.jpg"; // 

function App() {
  return (
    <Router>
      <div>
        <Header />
        <div className="container">
          <Routes>
            <Route path="/" element={<Auth />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/upload-resume" element={<ResumeUploader />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

// Header Component
function Header() {
  const location = useLocation();
  const navigate = useNavigate();

  // Login Checker
  const isLoggedIn = location.pathname === "/dashboard" || location.pathname === "/upload-resume";

  return (
    <header className="header">
      <img
        src={logo}
        alt="Job Forge Logo"
        className="logo"
        onClick={isLoggedIn ? () => navigate("/dashboard") : undefined}
        style={{ cursor: isLoggedIn ? "pointer" : "default" }}
      />
    </header>
  );
}

export default App;