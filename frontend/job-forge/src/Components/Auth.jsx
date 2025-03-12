import React, { useEffect, useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { UserContext } from "./UserContext";
import logo from "../Icons+Styling/Logo.png";

const Auth = () => {
  const [users, setUsers] = useState([]);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();
  const { setUser } = useContext(UserContext);

  useEffect(() => {
    fetch("http://localhost:5001/users")
      .then((response) => response.json())
      .then((data) => {
        if (Array.isArray(data.users)) {
          const extractedUsers = Array.isArray(data.users[0]) ? data.users[0] : data.users;
          setUsers(extractedUsers);
        } else {
          console.error("Unexpected response structure:", data);
        }
      })
      .catch((error) => console.error("Error fetching user data:", error));
  }, []);

  const handleLogin = () => {
    const user = users.find(
      (u) =>
        u.username?.trim().toLowerCase() === username.trim().toLowerCase() &&
        u.password?.trim() === password.trim()
    );

    if (user) {
      setMessage("Login Successful!");
      setUser(user);
      navigate("/home");
    } else {
      setMessage("Invalid Credentials");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div style={{ textAlign: "center", marginBottom: "20px" }}>
          <img src={logo} alt="Job Forge Logo" style={{ width: "100px", height: "auto" }} />
          <h2 style={{ color: "#BA5624;", fontSize: "24px", margin: "10px 0 0 0" }}>Job Forge</h2>
        </div>
        <h2>Login</h2>
        <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button onClick={handleLogin}>Login</button>
        <p className="message">{message}</p>
        <p>
          Don't have an account? <Link to="/register">Register here</Link>
        </p>
      </div>
    </div>
  );
};

export default Auth;
