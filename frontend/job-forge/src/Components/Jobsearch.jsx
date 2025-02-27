import { useState } from "react";

const JobSearch = () => {
  const [jobTitle, setJobTitle] = useState("");
  const [location, setLocation] = useState("");
  const [jobs, setJobs] = useState([]);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    setError(""); // Clear any previous errors

    try {
      const response = await fetch("http://localhost:5001/job_search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ job_title: jobTitle, location }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
      }

      setJobs(data.jobs);
    } catch (err) {
      setError(err.message);
      setJobs([]); // Clear job results if there's an error
    }
  };

  return (
    <div>
      <h2>Job Search</h2>
      <input
        type="text"
        placeholder="Job Title"
        value={jobTitle}
        onChange={(e) => setJobTitle(e.target.value)}
      />
      <input
        type="text"
        placeholder="Location"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {jobs.map((job, index) => (
          <li key={index}>
            <h3>{job.title}</h3>
            <p>{job.company} - {job.location}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default JobSearch;
