import "./App.css";
import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation, useNavigate } from "react-router-dom";
import Auth from "./Components/Auth.jsx";
import Dashboard from "./Components/Dashboard.jsx";
import ResumeUploader from "./Components/ResumeUploader.jsx";
import logo from "./JF_LOGO.jpg";
import { UserProvider } from "./Components/UserContext.jsx";

function App() {
  return (
    <Router>
      <UserProvider>
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
      </UserProvider>
    </Router>
  );
}


function Header() {
  const location = useLocation();
  const navigate = useNavigate();


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