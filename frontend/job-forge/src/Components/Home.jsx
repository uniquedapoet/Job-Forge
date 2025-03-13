import React, { useContext } from "react";
import MainLayout from "./MainLayout";
import { UserContext } from "./UserContext";
import "../Icons+Styling/MainContent.css";

const Home = ({ onLogout }) => {
  const { user } = useContext(UserContext); // Access user context

  return (
    <MainLayout onLogout={onLogout} title="Welcome to Job Forge" showWelcomeMessage={false}>
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%" }}>
        <div className="main-content-card">
          <h2 className="main-content-heading">Welcome to Job Forge</h2>
          {user && (
            <p style={{ marginBottom: "20px", textAlign: "center" }}>
              Welcome back, {user.first_name} {user.last_name}!
            </p>
          )}
          <p>Select an option from the sidebar to get started.</p>
        </div>
      </div>
    </MainLayout>
  );
};

export default Home;