import React from "react";
import Sidebar from "./Sidebar";

const MainLayout = ({ children, onLogout, title }) => {
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <Sidebar onLogout={onLogout} />
      <div style={{ flex: 1, padding: "20px" }}>
        {children}
      </div>
    </div>
  );
};

export default MainLayout;