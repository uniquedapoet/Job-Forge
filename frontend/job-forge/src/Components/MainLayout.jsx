import React from "react";
import Sidebar from "./Sidebar";

const MainLayout = ({ children, onLogout, title, sidebarVisible = true }) => {
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {sidebarVisible && <Sidebar onLogout={onLogout} />}
      <div style={{ flex: 1, padding: "20px" }}>
        {children}
      </div>
    </div>
  );
};

export default MainLayout;