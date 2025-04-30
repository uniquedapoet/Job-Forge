import React, { useContext } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { UserContext } from "./UserContext";
import { FaHome, FaSearch, FaUpload, FaSignOutAlt, FaDesktop, FaTimes } from "react-icons/fa";
import logo from "../Icons+Styling/Logo.png";
import "../Icons+Styling/Sidebar.css";

const Sidebar = ({ onLogout, onCloseSidebar }) => {
  const { user } = useContext(UserContext);
  const navigate = useNavigate();

  const isMobile = window.innerWidth <= 768;
/* I HATE MOBILE RESPONSIVENESS!!!!!*/
  return (
    <div className="sidebar">
      {isMobile && (
        <button
          onClick={onCloseSidebar}
          style={{
            alignSelf: 'flex-end',
            background: 'none',
            border: 'none',
            fontSize: '1.5rem',
            color: '#ba5624',
            cursor: 'pointer',
            marginBottom: '1rem'
          }}
        >
          <FaTimes />
        </button>
      )}

      <div>
        <div className="sidebar-logo">
          <img
            src={logo}
            alt="Job Forge Logo"
            onClick={() => navigate("/home")}
            style={{ cursor: "pointer" }}
          />
          <h2>Job Forge</h2>
        </div>

        <nav>
          <ul className="sidebar-nav">
            <li>
              <NavLink
                to="/home"
                className={({ isActive }) => (isActive ? "active" : "")}
              >
                <FaHome className="icon" /> Home
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/dashboard"
                className={({ isActive }) => (isActive ? "active" : "")}
              >
                <FaDesktop className="icon" /> Dashboard
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/job-search"
                className={({ isActive }) => (isActive ? "active" : "")}
              >
                <FaSearch className="icon" /> Job Search
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/upload-resume"
                className={({ isActive }) => (isActive ? "active" : "")}
              >
                <FaUpload className="icon" /> Upload Resume
              </NavLink>
            </li>
          </ul>
        </nav>
      </div>

      <div className="sidebar-logout">
        <p>{user?.email}</p>
        <button onClick={onLogout}>
          <FaSignOutAlt style={{ marginRight: "10px", fontSize: "18px" }} /> Sign Out
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
