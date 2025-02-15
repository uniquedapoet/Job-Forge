import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Auth = () => {
  const [users, setUsers] = useState([]);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://localhost:5001/users")
      .then((response) => response.json())
      .then((data) => {
        if (Array.isArray(data.users)) {
          const extractedUsers = Array.isArray(data.users[0])
            ? data.users[0]
            : data.users;
          setUsers(extractedUsers);
        } else {
          console.error("Unexpected response structure:", data);
        }
      })
      .catch((error) => {
        console.error("Error fetching user data:", error);
      });
  }, []);

  const handleLogin = () => {
    const user = users.find(
      (u) =>
        u.username?.trim().toLowerCase() === username.trim().toLowerCase() &&
        u.password?.trim() === password.trim()
    );

    if (user) {
      setMessage("Login Successful!");
      navigate("/dashboard");
    } else {
      setMessage("Invalid Credentials");
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "80vh",
      }}
    >
      <div className="card" style={{ maxWidth: "400px", width: "100%", textAlign: "center" }}>
        <h2>Login</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleLogin}>Login</button>
        <p className="message">{message}</p>
      </div>
    </div>
  );
};

export default Auth;