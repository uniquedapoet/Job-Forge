import React, { useState } from "react";

const JobSearch = ({ onSearch }) => {
  const [jobTitle, setJobTitle] = useState("");
  const [location, setLocation] = useState("");

  const handleSearch = () => {
    onSearch(jobTitle, location);
  };

  return (
    <div style={{ marginBottom: "20px" }}>
      <input
        type="text"
        placeholder="Job Title"
        value={jobTitle}
        onChange={(e) => setJobTitle(e.target.value)}
        style={{ marginRight: "10px", padding: "5px" }}
      />
      <input
        type="text"
        placeholder="Location"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        style={{ marginRight: "10px", padding: "5px" }}
      />
      <button onClick={handleSearch} style={{ padding: "5px 10px" }}>
        Search
      </button>
    </div>
  );
};

export default JobSearch;