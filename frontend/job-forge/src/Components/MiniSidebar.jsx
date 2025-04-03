import React from "react";
import { FaHome, FaSearch, FaUpload, FaDesktop } from "react-icons/fa";
import logo from "../Icons+Styling/Logo.png";
import "../Icons+Styling/Sidebar.css";

const MiniSidebar = ({ onExpand }) => {
  return (
    <div className="mini-sidebar">
      <div className="mini-sidebar-content">
        <div className="sidebar-logo" onClick={onExpand}>
          <img src={logo} alt="Job Forge Logo" />
        </div>

        <nav>
          <ul className="sidebar-nav">
            <li>
              <a href="/home">
                <FaHome className="icon" />
              </a>
            </li>
            <li>
              <a href="/dashboard">
                <FaDesktop className="icon" />
              </a>
            </li>
            <li>
              <a href="/job-search">
                <FaSearch className="icon" />
              </a>
            </li>
            <li>
              <a href="/upload-resume">
                <FaUpload className="icon" />
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
};

export default MiniSidebar;