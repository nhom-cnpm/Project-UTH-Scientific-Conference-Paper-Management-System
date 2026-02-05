import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";

export default function Login() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (form.username === "reviewer") {
      navigate("/reviewer");
    } else if (form.username === "chair") {
      navigate("/chair");
    } else {
      alert("Invalid username or password");
    }
  };

  return (
    <div className="login-container">
      <div className="header-bar">UTH - COMFMS</div>
      <div className="login-overlay">
        <div className="login-box">
          <h2>LOG IN TO THE SYSTEM</h2>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              name="username"
              placeholder="Email / Username"
              value={form.username}
              onChange={handleChange}
              required
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={form.password}
              onChange={handleChange}
              required
            />
            <button type="submit">LOGIN</button>
          </form>
          <p className="forgot-password">FORGOT PASSWORD?</p>
        </div>
      </div>
    </div>
  );
}
