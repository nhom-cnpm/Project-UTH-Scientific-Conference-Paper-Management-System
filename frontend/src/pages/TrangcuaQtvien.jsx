import React from "react";
import { Link } from "react-router-dom";
import "../styles/Qtrv.css";

const Home = () => {
  // Giả lập thông tin user đang đăng nhập
  const user = {
    id: 1,
    name: "Quản trị viên"
  };

  return (
    <div className="home-container">
      {/* Header */}
      <header className="header">
        <Link to="/" className="logo-link">
        <div className="logo">UTH - COMFMS</div>
        </Link>

        <nav className="nav">
          <Link to="/guide">HƯỚNG DẪN</Link>
          <Link to="/result">KẾT QUẢ</Link>
          <Link to="/rule">QUY ĐỊNH</Link>
        </nav>

        <button className="admin-btn">{user.name}</button>
      </header>

      {/* Hero */}
      <section className="hero">
        <h1>
          Thúc đẩy sáng tạo thông qua <br />
          <span>Nghiên cứu khoa học</span>
        </h1>
        <p>
          Nền tảng nộp bài, quản lý và đánh giá các báo cáo khoa học
          dành cho sinh viên và giảng viên.
        </p>
      </section>

      {/* Welcome */}
      <section className="welcome-section">
        <div className="welcome-box">
          <p>
            Chào mừng <b>{user.name}</b> trở lại
          </p>

          <Link to="/conference-manage" className="edit-link">
          Tại đây để chỉnh sửa
          </Link>

        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        Trường Đại học Giao thông vận tải TP.HCM
      </footer>
    </div>
  );
};

export default Home;