import React from "react";
import "./Icons+Styling/App.css";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Auth from "./Components/Auth.jsx";
import Home from "./Components/Home.jsx";
import ResumeUploader from "./Components/ResumeUploader.jsx";
import ResumeEditor from "./Components/ResumeEditor.jsx";
import JobSearch from "./Components/Jobsearch.jsx";
import Dashboard from "./Components/Dashboard.jsx";
import { UserProvider } from "./Components/UserContext.jsx";
import Register from "./Components/Register.jsx";

function App() {
  const handleLogout = () => {
    localStorage.removeItem("user");
    window.location.href = "/";
  };

  return (
    <Router>
      <UserProvider>
        <div>
          <div className="container">
            <Routes>
              <Route path="/" element={<Auth />} />
              <Route path="/register" element={<Register />} />
              <Route path="/home" element={<Home onLogout={handleLogout} />} />
              <Route path="/upload-resume" element={<ResumeUploader onLogout={handleLogout} />} />
              <Route path="/edit-resume" element={<ResumeEditor onLogout={handleLogout} />} />
              <Route path="/job-search" element={<JobSearch onLogout={handleLogout} />} />
              <Route path="/dashboard" element={<Dashboard onLogout={handleLogout} />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </div>
        </div>
      </UserProvider>
    </Router>
  );
}

export default App;
