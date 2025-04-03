import React, { useEffect, useState, useContext } from "react";
import MainLayout from "./MainLayout";
import { UserContext } from "./UserContext";
import "../Icons+Styling/MainContent.css";
import "../Icons+Styling/Sidebar.css";
import logo from "../Icons+Styling/Logo.png";

const ResumeEditor = ({ onLogout }) => {
  const { user } = useContext(UserContext);
  const [resumeUrl, setResumeUrl] = useState("");
  const [message, setMessage] = useState({ text: "", isError: false });
  const [sidebarVisible, setSidebarVisible] = useState(true);
  const [suggestions, setSuggestions] = useState([
    "Consider adding more action verbs to your work experience",
    "Your education section could include relevant coursework",
    "Try to quantify your achievements with numbers where possible"
  ]);

  useEffect(() => {
    const fetchResumeUrl = async () => {
      if (user?.id) {
        try {
          const url = `http://localhost:5001/resumes/view/${user.id}`;
          setResumeUrl(url);
        } catch (error) {
          setMessage({ text: "Error fetching resume URL.", isError: true });
        }
      }
    };
    fetchResumeUrl();
  }, [user]);

  const toggleSidebar = () => {
    setSidebarVisible(!sidebarVisible);
  };

  return (
    <MainLayout onLogout={onLogout} title="Resume Editor" sidebarVisible={sidebarVisible}>
      <div className="resume-editor-container">
        <button 
          onClick={toggleSidebar}
          className="sidebar-toggle-btn"
          style={{
            position: 'fixed',
            left: sidebarVisible ? '280px' : '0',
            top: '20px',
            zIndex: 1000,
            padding: '10px',
            background: '#ba5624',
            border: 'none',
            borderRadius: '0 5px 5px 0',
            cursor: 'pointer',
            transition: 'left 0.3s ease',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <img 
            src={logo} 
            alt="Toggle Sidebar" 
            style={{ 
              width: '30px', 
              height: '30px',
              filter: 'brightness(0) invert(1)'
            }} 
          />
        </button>
        
        <div className="resume-content-wrapper">
          <div className="pdf-viewer-container">
            <h2>Your Resume</h2>
            {resumeUrl ? (
              <object
                data={`${resumeUrl}#toolbar=0&navpanes=0`}
                type="application/pdf"
                style={{ width: "100%", height: "80vh", border: "none" }}
              >
                <p>Your browser doesn't support PDF viewing. <a href={resumeUrl}>Download instead</a></p>
              </object>
            ) : (
              <p>Loading resume...</p>
            )}
            {message.text && (
              <p style={{ color: message.isError ? "red" : "green", marginTop: "10px" }}>
                {message.text}
              </p>
            )}
          </div>

          <div className="suggestions-container">
            <h2>Suggestions</h2>
            <div className="suggestions-list">
              {suggestions.map((suggestion, index) => (
                <div key={index} className="suggestion-card">
                  <p>{suggestion}</p>
                  <button className="apply-suggestion-btn">Apply</button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default ResumeEditor;