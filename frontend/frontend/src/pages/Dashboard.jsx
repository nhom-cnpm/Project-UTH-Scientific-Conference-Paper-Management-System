import React from "react";
import { Link } from "react-router-dom";
import "../styles/Dashboard.css";

const Dashboard = () => {
  return (
    <div className="dashboard-page">
      {/* ===== HEADER ===== */}
      <header className="dashboard-header">
        <div className="logo">UTH - COMFMS</div>

        <nav className="dashboard-nav">
          <span>HƯỚNG DẪN</span>
          <span>KẾT QUẢ</span>
          <span>QUY ĐỊNH</span>
        </nav>

        <div className="admin-badge">TÊN QUẢN TRỊ VIÊN</div>
      </header>

      {/* ===== MAIN ===== */}
      <main className="dashboard-main">
        <h1>
          Thúc đẩy sáng tạo thông qua <br />
          <span>Nghiên cứu khoa học</span>
        </h1>

        <p className="dashboard-desc">
          Nền tảng nộp bài, quản lý và đánh giá các báo cáo khoa học
          dành cho sinh viên và giảng viên.
        </p>

        <div className="dashboard-card">
          <p>
            Chào mừng <b>“Tên quản trị viên”</b> trở lại
          </p>
           <Link to="/ConferenceManager">Tại đây</Link>, để chỉnh sửa
        </div>
      </main>

      {/* ===== FOOTER ===== */}
      <footer className="dashboard-footer">
        Trường Đại học Giao thông vận tải thành phố Hồ Chí Minh
      </footer>
    </div>
  );
};

export default Dashboard;
