import "./App.css";
import Auth from "./auth";
import React, { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  
  return (
    <div>
      <h1>Flask + React Integration</h1>
      <p>Backend Response: {message}</p>
      <Auth />
    </div>
  );
}

export default App;
