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
      /** * NOTE: Vì không dùng Backend, chúng ta giả lập dữ liệu trả về
       * dựa trên sơ đồ Admin, Chair, Reviewer, Author, Guest.
       */
      const mockUsers = [
        {
          username: "admin",
          password: "123",
          role: "admin",
          displayName: "Administrator",
        },
        {
          username: "chair",
          password: "123",
          role: "chair",
          displayName: "Program Chair",
        },
        {
          username: "reviewer",
          password: "123",
          role: "reviewer",
          displayName: "Reviewer PC",
        },
        {
          username: "author",
          password: "123",
          role: "author",
          displayName: "Author",
        },
      ];

      // Tìm tài khoản khớp với form
      const user = mockUsers.find(
        (u) => u.username === form.username && u.password === form.password,
      );

      // Giả lập độ trễ mạng 0.5 giây
      await new Promise((resolve) => setTimeout(resolve, 500));

      if (!user) {
        throw new Error("Invalid username or password");
      }

      // Giả lập cấu trúc data trả về từ API
      const data = {
        token: "fake-jwt-token-for-testing",
        role: user.role,
        username: user.displayName,
      };

      // ===== LƯU THÔNG TIN =====
      localStorage.setItem("token", data.token);
      localStorage.setItem("role", data.role);
      localStorage.setItem("username", data.username);

      // ===== CHUYỂN TRANG THEO ROLE (Khớp với App.jsx) =====
      switch (data.role) {
        case "admin":
          navigate("/admin/dashboard"); // Cần đảm bảo App.jsx có route này
          break;

        case "reviewer":
          navigate("/reviewer/assigned"); // Theo đường dẫn bạn đã fix lỗi import
          break;

        case "chair":
          navigate("/chair/workflow"); // Theo sơ đồ Chair Workflow của bạn
          break;

        case "author":
          navigate("/author/submissions");
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

          {error && (
            <p className="error" style={{ color: "red", marginTop: "10px" }}>
              {error}
            </p>
          )}

          <p className="forgot-password">FORGOT PASSWORD?</p>
        </div>
      </div>
    </div>
  );
}
