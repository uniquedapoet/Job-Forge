import React, { useEffect } from "react";
import "../Icons+Styling/MainContent.css";

const JobModal = ({ job, onClose, onSaveJob, isSaved, isProcessing }) => {
  useEffect(() => {
    document.body.classList.add("hide-hamburger");
    return () => {
      document.body.classList.remove("hide-hamburger");
    };
  }, []);

  const formatDescription = (description) => {
    if (!description) return null;

    let cleaned = description
      .replace(/\\&/g, '&')
      .replace(/\\\d+/g, '')
      .replace(/(\d)\\/g, '$1')
      .replace(/(\d)\s?-\s?(\d)/g, '$1-$2')
      .replace(/\\n/g, '\n')
      .replace(/\\-/g, '-')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*/g, '• ')
      .replace(/\t\+/g, '  • ')
      .replace(/\n{2,}/g, '\n\n')
      .trim();

    const paragraphs = cleaned.split('\n\n').filter(p => p.trim().length > 0);

    return paragraphs.map((paragraph, index) => (
      <p
        key={index}
        className="job-description"
        style={{ marginBottom: '1rem' }}
        dangerouslySetInnerHTML={{ __html: paragraph }}
      />
    ));
  };

  const formatJobType = (type) => {
    if (!type) return null;
    const map = {
      fulltime: 'Full-Time',
      parttime: 'Part-Time',
      contract: 'Contract',
      internship: 'Internship',
      freelance: 'Freelance',
      temporary: 'Temporary',
    };
    return map[type.toLowerCase()] || type.charAt(0).toUpperCase() + type.slice(1);
  };

  return (
    <div
      className="modal-overlay"
      onClick={(e) => {
        if (e.target.classList.contains("modal-overlay")) {
          onClose();
        }
      }}
    >
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>
          &times;
        </button>

        <div className="modal-header">
          <h2>{job.title}</h2>
          <h3>{job.company}</h3>
          <p className="job-location">{job.location}</p>
        </div>
        {job.job_url && (
              <a
                href={job.job_url_direct}
                target="_blank"
                rel="noopener noreferrer"
                className="apply-button"
                style={{
                  backgroundColor: "#6c757d",
                  width:'305px'

                }}
              >
                <i className="fas fa-external-link-alt"></i>
                View Original Posting
              </a>
            )}

            {onSaveJob && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onSaveJob(job);
                }}
                className="apply-button"
                style={{
                  backgroundColor: isSaved ? "#6c757d" : "#ba5624",
                  width:'342px'

                }}
                disabled={isProcessing}
              >
                <i className={isSaved ? "fas fa-trash-alt" : "fas fa-bookmark"}></i>
                {isProcessing ? "Processing..." : (isSaved ? "Remove" : "Save")}
              </button>
            )}

        <div className="job-meta">
          {job.job_type && (
            <div className="meta-item">
              <i className="fas fa-briefcase"></i>
              <span><strong>Job Type:</strong> {formatJobType(job.job_type)}</span>
            </div>
          )}
          {job.date_posted && (
            <div className="meta-item">
              <i className="fas fa-calendar-alt"></i>
              <span><strong>Posted:</strong> {job.date_posted}</span>
            </div>
          )}
        </div>

        <div className="modal-body">
          <div className="job-section">
            <h4 className="section-title">
              <i className="fas fa-file-alt"></i>
              Description:
            </h4>
            <div className="job-description">
              {formatDescription(job.description)}
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <div className="action-buttons">
            {/* {job.job_url && (
              <a
                href={job.job_url_direct}
                target="_blank"
                rel="noopener noreferrer"
                className="apply-button"
                style={{
                  backgroundColor: "#6c757d",
                }}
              >
                <i className="fas fa-external-link-alt"></i>
                View Original Posting
              </a>
            )}

            {onSaveJob && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onSaveJob(job);
                }}
                className="apply-button"
                style={{
                  backgroundColor: isSaved ? "#6c757d" : "#ba5624",
                }}
                disabled={isProcessing}
              >
                <i className={isSaved ? "fas fa-trash-alt" : "fas fa-bookmark"}></i>
                {isProcessing ? "Processing..." : (isSaved ? "Remove" : "Save")}
              </button>
            )} */}
            <button
              onClick={onClose}
              className="close-modal-button"
            >
              <i className="fas fa-times"></i>
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobModal;
