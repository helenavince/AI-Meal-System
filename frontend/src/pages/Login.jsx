import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const handleLogin = () => {

    fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        email: email,
        password: password
      })
    })
      .then(response => response.json())
      .then(data => {

        if (data.success) {

          // Save student information
          localStorage.setItem(
            "student",
            JSON.stringify(data)
          );

          alert("Login successful!");

          navigate("/booking");

        } else {

          alert("Invalid email or password");

        }

      })
      .catch(error => {

        console.error("Login error:", error);
        alert("Unable to connect to server");

      });

  };

  return (

    <div className="dashboard">

      <h1>Student Login</h1>

      <div className="login-container">

        <input
          type="email"
          placeholder="Enter email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <br /><br />

        <input
          type="password"
          placeholder="Enter password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <br /><br />

        <button onClick={handleLogin}>
          Login
        </button>

      </div>

    </div>

  );
}

export default Login;