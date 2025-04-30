import React, { useEffect, useState } from "react";
import Sidebar from "./Sidebar";
import { FaBars } from "react-icons/fa";
import logo from "../Icons+Styling/Logo.png";

const MainLayout = ({
  children,
  onLogout,
  sidebarVisible: controlledSidebarVisible,
  onToggleSidebar,
}) => {
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);
  const [internalSidebarVisible, setInternalSidebarVisible] = useState(
    !isMobile
  );

  const sidebarVisible =
    controlledSidebarVisible !== undefined
      ? controlledSidebarVisible
      : internalSidebarVisible;
  const toggleSidebar =
    onToggleSidebar || (() => setInternalSidebarVisible((prev) => !prev));

  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth <= 768;
      setIsMobile(mobile);
      if (!onToggleSidebar) {
        setInternalSidebarVisible(!mobile);
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [onToggleSidebar]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: isMobile ? "column" : "row",
        height: "100vh",
        position: "relative",
      }}
    >
      {!sidebarVisible && (
        <button
          className="sidebar-toggle-btn"
          onClick={toggleSidebar}
          style={{
            position: "absolute",
            top: 20,
            left: 20,
            zIndex: 1001,
            backgroundColor: "#ba5624",
            border: "none",
            borderRadius: "8px",
            padding: "10px",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <img
            src={logo}
            alt="Toggle Sidebar"
            style={{
              width: "24px",
              height: "24px",
              filter: "brightness(0) invert(1)",
            }}
          />
        </button>
      )}

      {/* Mobile Sidebar Overlay */}
      {isMobile && sidebarVisible && (
        <div
          onClick={toggleSidebar}
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            backgroundColor: "rgba(0,0,0,0.3)",
            zIndex: 1000,
          }}
        />
      )}

      {/* Sidebar */}
      {sidebarVisible && (
        <Sidebar
          onLogout={onLogout}
          onCloseSidebar={toggleSidebar}
          isVisible={sidebarVisible}
        />
      )}

      <div
        style={{
          flex: 1,
          padding: "20px",
          overflowY: "auto",
        }}
      >
        {children}
      </div>
    </div>
  );
};

export default MainLayout;
