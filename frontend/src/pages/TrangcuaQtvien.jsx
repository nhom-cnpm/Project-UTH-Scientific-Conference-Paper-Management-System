import React from "react";
import { Link } from "react-router-dom";
import "../styles/Qtrv.css";

const Home = () => {
  return (
    <div className="home-container">
      {/* Header */}
      <header className="header">
        <div className="logo">UTH - COMFMS</div>

        <nav className="nav">
          <Link to="/guide">HƯỚNG DẪN</Link>
          <Link to="/result">KẾT QUẢ</Link>
          <Link to="/rule">QUY ĐỊNH</Link>
        </nav>

        <button className="admin-btn">TÊN QUẢN TRỊ VIÊN</button>
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
            Chào mừng <b>“Tên quản trị viên”</b> trở lại
          </p>

          <Link
            to="/dashboard/conference-manage"
            className="ConferenceManager"
          >
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
