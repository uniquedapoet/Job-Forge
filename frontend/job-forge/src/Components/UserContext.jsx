import React, { createContext, useState, useEffect } from "react";

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  // Retrieve user data from localStorage on initial load
  const storedUser = JSON.parse(localStorage.getItem("user"));
  const [user, setUser] = useState(storedUser || null);
  const [savedJobs, setSavedJobs] = useState(storedUser?.savedJobs || []);
  const [scores, setScores] = useState(storedUser?.scores || {}); // Add scores state

  // Save user data to localStorage whenever it changes
  useEffect(() => {
    if (user) {
      const updatedUser = { ...user, savedJobs, scores }; // Include savedJobs and scores in the user object
      localStorage.setItem("user", JSON.stringify(updatedUser));
    } else {
      localStorage.removeItem("user");
    }
  }, [user, savedJobs, scores]);

  return (
    <UserContext.Provider value={{ user, setUser, savedJobs, setSavedJobs, scores, setScores }}>
      {children}
    </UserContext.Provider>
  );
};