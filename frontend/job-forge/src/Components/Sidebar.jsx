import React, { useContext } from "react";
import { NavLink } from "react-router-dom"; 
import { UserContext } from "./UserContext";
import { FaHome, FaSearch, FaUpload, FaSignOutAlt } from "react-icons/fa";
import logo from "../Icons+Styling/Logo.png";
import "../Icons+Styling/Sidebar.css";

const Sidebar = ({ onLogout }) => {
  const { user } = useContext(UserContext);

  return (
    <div className="sidebar">
      <div>
        <div className="sidebar-logo">
          <img src={logo} alt="Job Forge Logo" />
          <h2>Job Forge</h2>
        </div>

        <nav>
          <ul className="sidebar-nav">
            <li>
              <NavLink
                to="/dashboard"
                className={({ isActive }) => (isActive ? "active" : "")}
              >
                <FaHome className="icon" /> Home
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