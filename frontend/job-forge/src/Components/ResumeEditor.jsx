import React, { useEffect, useState, useContext } from "react";
import MainLayout from "./MainLayout";
import { UserContext } from "./UserContext";
import { useLocation } from "react-router-dom";
import "../Icons+Styling/MainContent.css";
import "../Icons+Styling/Sidebar.css";
import logo from "../Icons+Styling/Logo.png";

const ResumeEditor = ({ onLogout }) => {
  const { user } = useContext(UserContext);
  const location = useLocation();
  const selectedJobId = location.state?.selectedJobId || null;
  const [resumeUrl, setResumeUrl] = useState("");
  const [message, setMessage] = useState({ text: "", isError: false });
  const [sidebarVisible, setSidebarVisible] = useState(false);
  const [generalSuggestions, setGeneralSuggestions] = useState([]);
  const [jobSpecificSuggestions, setJobSpecificSuggestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("general");

  useEffect(() => {
    const fetchData = async () => {
      if (!user?.id || !selectedJobId) return;

      setLoading(true);
      try {
        // Fetch both
        const [generalRes, jobSpecificRes] = await Promise.all([
          fetch(`https://job-forge.ngrok.app/resumes/general/${user.id}`),
          fetch(
            `https://job-forge.ngrok.app/resumes/job_specific_suggestions/${selectedJobId}/${user.id}`
          ),
        ]);

        const generalData = await generalRes.json();
        const jobSpecificData = await jobSpecificRes.json();
        console.log(jobSpecificData.suggestions.JobBasedSuggestions);

        if (generalData.suggestions) {
          setGeneralSuggestions(
            generalData.suggestions.GeneralSuggestions || []
          );
        }
        if (jobSpecificData.suggestions) {
          setJobSpecificSuggestions(
            jobSpecificData.suggestions.JobBasedSuggestions || []
          );
        }
      } catch (error) {
        setMessage({ text: "Error fetching suggestions.", isError: true });
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user, selectedJobId]);

  useEffect(() => {
    const fetchResumeUrl = async () => {
      if (user?.id) {
        try {
          const url = `https://job-forge.ngrok.app/resumes/view/${user.id}`;
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
    <MainLayout
      onLogout={onLogout}
      title="Resume Editor"
      sidebarVisible={sidebarVisible}
      onToggleSidebar={toggleSidebar}
    >
      <div className="resume-editor-container">
        {/* <button
          onClick={toggleSidebar}
          className="sidebar-toggle-btn"
          style={{
            position: "fixed",
            left: sidebarVisible ? "280px" : "0",
            top: "20px",
            zIndex: 1000,
            padding: "10px",
            background: "#ba5624",
            border: "none",
            borderRadius: "0 5px 5px 0",
            cursor: "pointer",
            transition: "left 0.3s ease",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <img
            src={logo}
            alt="Toggle Sidebar"
            style={{
              width: "30px",
              height: "30px",
              filter: "brightness(0) invert(1)",
            }}
          />
        </button> */}

        <div className="resume-content-wrapper">
          <div className="pdf-viewer-container">
            <h2>Your Resume</h2>
            {resumeUrl ? (
              <object
                data={`${resumeUrl}#toolbar=0&navpanes=0`}
                type="application/pdf"
                style={{ width: "100%", height: "80vh", border: "none" }}
              >
                <p>
                  Your browser doesn't support PDF viewing.{" "}
                  <a href={resumeUrl}>Download instead</a>
                </p>
              </object>
            ) : (
              <p>Loading resume...</p>
            )}
            {message.text && (
              <p
                style={{
                  color: message.isError ? "red" : "green",
                  marginTop: "10px",
                }}
              >
                {message.text}
              </p>
            )}
          </div>

          <div className="suggestions-container">
            <div className="suggestions-tabs">
              <button
                className={`tab-button ${
                  activeTab === "general" ? "active" : ""
                }`}
                onClick={() => setActiveTab("general")}
              >
                General Suggestions
              </button>

              <button
                className={`tab-button ${activeTab === "job" ? "active" : ""}`}
                onClick={() => setActiveTab("job")}
              >
                Job-Specific Suggestions
              </button>
            </div>

            {loading ? (
              <div className="suggestions-loading">
                <p>Loading suggestions...</p>
              </div>
            ) : (
              <div className="suggestions-content">
                {activeTab === "general" ? (
                  <div className="suggestions-list">
                    {generalSuggestions.length > 0 ? (
                      generalSuggestions.map((suggestion, index) => (
                        <div
                          key={`general-${index}`}
                          className="suggestion-card"
                        >
                          <p>
                            {suggestion.replace(/^(\w)/, (c) =>
                              c.toUpperCase()
                            )}
                          </p>
                        </div>
                      ))
                    ) : (
                      <p>No general suggestions available.</p>
                    )}
                  </div>
                ) : (
                  <div className="suggestions-list">
                    {jobSpecificSuggestions ? (
                      <>
                        {jobSpecificSuggestions.TechnologiesToAdd.length >
                          0 && (
                          <div className="suggestion-section">
                            <h3>Technologies to Add</h3>
                            {jobSpecificSuggestions.TechnologiesToAdd.map(
                              (tech, index) => (
                                <div
                                  key={`tech-${index}`}
                                  className="suggestion-card"
                                >
                                  <p>{tech}</p>
                                </div>
                              )
                            )}
                          </div>
                        )}

                        {jobSpecificSuggestions.SoftSkillsToAdd.length > 0 && (
                          <div className="suggestion-section">
                            <h3>Soft Skills to Add</h3>
                            {jobSpecificSuggestions.SoftSkillsToAdd.map(
                              (skill, index) => (
                                <div
                                  key={`soft-${index}`}
                                  className="suggestion-card"
                                >
                                  <p>
                                    {skill.replace(/^(\w)/, (c) =>
                                      c.toUpperCase()
                                    )}
                                  </p>
                                </div>
                              )
                            )}
                          </div>
                        )}

                        {jobSpecificSuggestions.CertificationsOrFrameworksToAdd
                          .length > 0 && (
                          <div className="suggestion-section">
                            <h3>Certifications or Frameworks to Add</h3>
                            {jobSpecificSuggestions.CertificationsOrFrameworksToAdd.map(
                              (cert, index) => (
                                <div
                                  key={`cert-${index}`}
                                  className="suggestion-card"
                                >
                                  <p>
                                    {cert.replace(/^(\w)/, (c) =>
                                      c.toUpperCase()
                                    )}
                                  </p>
                                </div>
                              )
                            )}
                          </div>
                        )}

                        {jobSpecificSuggestions.EasyKeywordWins.length > 0 && (
                          <div className="suggestion-section">
                            <h3>Easy Keyword Wins</h3>
                            {jobSpecificSuggestions.EasyKeywordWins.map(
                              (keyword, index) => (
                                <div
                                  key={`keyword-${index}`}
                                  className="suggestion-card"
                                >
                                  <p>
                                    {keyword.replace(/^(\w)/, (c) =>
                                      c.toUpperCase()
                                    )}
                                  </p>
                                </div>
                              )
                            )}
                          </div>
                        )}
                      </>
                    ) : (
                      <p>No job-specific suggestions available.</p>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default ResumeEditor;
