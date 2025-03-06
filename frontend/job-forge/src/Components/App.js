import "./App.css";
import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useLocation,
  useNavigate,
} from "react-router-dom";
import Auth from "./auth.js";
import Dashboard from "./dashboard.js";
import ResumeUploader from "./resume_uploader.jsx";
import logo from "./JF_LOGO.jpg"; //
import JobSearch from "./Jobsearch.jsx";
import { UserProvider } from "./UserContext.jsx";

function App() {
  return (
    <Router>
      <UserProvider>
        <div>
          <Header />
          <JobSearch />
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

// Header Component
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
