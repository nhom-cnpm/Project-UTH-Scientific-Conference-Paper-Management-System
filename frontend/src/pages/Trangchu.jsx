import React from "react";
import { Link } from "react-router-dom";
import "../styles/Trangchu.css";

const Home = () => {
  return (
    <div className="landing-container">

      {/* Navbar */}
      <div className="navbar">
        <div className="logo">UTH - COMFMS</div>  

        <div className="nav-links">
          <a href="#">HƯỚNG DẪN</a>
          <a href="#">KẾT QUẢ</a>
          <a href="#">QUY ĐỊNH</a>

          <Link to="/login" className="btn-login">
            ĐĂNG NHẬP
          </Link>
        </div>
      </div>

      {/* Hero */}
      <div className="hero">
        <h1>Thúc đẩy sáng tạo thông qua</h1>
        <div className="highlight">Nghiên cứu khoa học</div>
        <p className="subtitle">
          Nền tảng nộp bài, quản lý và đánh giá các báo cáo khoa học dành cho sinh viên và giảng viên.
        </p>
      </div>

      {/* Events */}
      <div className="events-section">
        <div className="section-header">
          <h2>Các sự kiện khoa học đang diễn ra</h2>
          <a href="#" className="view-all">Xem tất cả →</a>
        </div>

        <div className="event-grid">
          <EventCard
            status="Đang mở"
            badgeClass="open"
            timeLeft="Còn 5 ngày"
            title="Nghiên cứu khoa học và đổi mới sáng tạo"
            desc="Chủ đề: Ứng dụng công nghệ vào đời sống"
            deadline="11/01/2026"
          />

          <EventCard
            status="Sắp mở"
            badgeClass="upcoming"
            timeLeft="Bắt đầu: 01/02"
            title="Đề tài 2:"
            desc="Chủ đề: Phương pháp tìm kiếm và đánh giá"
            deadline="31/02/2026"
          />
        </div>
      </div>

      {/* Footer */}
      <div className="footer">
        Trường Đại học Giao thông vận tải TP.HCM
      </div>

    </div>
  );
};

const EventCard = ({ status, badgeClass, timeLeft, title, desc, deadline }) => (
  <div className="event-card">
    <div className="card-top">
      <span className={`badge ${badgeClass}`}>{status}</span>
      <span className="red-text">⏱ {timeLeft}</span>
    </div>

    <h3 className="card-title">{title}</h3>
    <p className="card-desc">{desc}</p>

    <div className="card-footer">
      <span>Hạn cuối: {deadline}</span>
      <button className="btn-detail">Chi tiết</button>
    </div>
  </div>
);

export default Home;
