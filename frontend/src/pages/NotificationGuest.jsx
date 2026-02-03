import React from "react";
import SidebarGuest from "../components/SidebarGuest";
import NotificationTable from "../components/NotificationTable";
import "../styles/Notification.css"; // File CSS mình đã cung cấp ở câu trước

const NotificationPage = () => {
  // Giả sử sau này bạn lấy dữ liệu từ API ở đây
  const data = [];

  return (
    <div className="dashboard-container">
      <SidebarGuest />

      <div className="main-content">
        <header className="top-header">
          <div className="user-info">
            <span className="user-name">Nguyen Van A</span>
            <i className="fas fa-caret-down"></i>
          </div>
        </header>

        <div className="content-body">
          <h2 className="content-title">Your notification list</h2>
          {/* Sử dụng Component bạn đã tạo */}
          <NotificationTable notifications={data} />
        </div>
      </div>
    </div>
  );
};

export default NotificationPage;
