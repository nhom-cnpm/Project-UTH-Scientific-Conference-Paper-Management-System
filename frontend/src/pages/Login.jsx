import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";

export default function Login() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:3000/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.message || "Login failed");
      }

      // ===== LƯU THÔNG TIN =====
      localStorage.setItem("token", data.token);
      localStorage.setItem("role", data.role);
      localStorage.setItem("username", data.username);

      // ===== CHUYỂN TRANG THEO ROLE =====
      switch (data.role) {
        case "admin":
          navigate("/admin");
          break;

        case "reviewer":
          navigate("/reviewer");
          break;

        case "chair":
          navigate("/chair");
          break;

        case "student":
          navigate("/student");
          break;

        default:
          navigate("/");
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
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

            <button type="submit" disabled={loading}>
              {loading ? "Loading..." : "LOGIN"}
            </button>
          </form>

          {error && <p className="error">{error}</p>}

          <p className="forgot-password">FORGOT PASSWORD?</p>
        </div>
      </div>
    </div>
  );
}
