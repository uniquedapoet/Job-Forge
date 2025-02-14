import React, { useEffect, useState } from "react";

const Auth = () => {
  const [users, setUsers] = useState([]);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  // Fetch users from backend
  useEffect(() => {
    fetch("http://localhost:5001/users")
      .then((response) => response.json())
      .then((data) => {
        console.log("Fetched user data:", data);

        // Ensure data.users is an array and flatten it if necessary
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

  // Handle Login
  const handleLogin = () => {
    console.log("Users loaded:", users);
    console.log("Entered:", username.trim(), password.trim());

    const user = users.find(
      (u) =>
        u.username?.trim().toLowerCase() === username.trim().toLowerCase() &&
        u.password?.trim() === password.trim()
    );

    if (user) {
      setMessage("Login Successful!");
    } else {
      setMessage("Invalid Credentials");
    }
  };

  return (
    <div>
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
      <p>{message}</p>
    </div>
  );
};

export default Auth;
