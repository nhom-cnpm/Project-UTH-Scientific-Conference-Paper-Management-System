import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "../styles/SidebarAuthor.css"; // Đảm bảo file CSS này tồn tại

const SidebarAuthor = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // Cấu trúc Menu khớp với các Route bạn đã khai báo trong App.jsx
  const menuItems = [
    { name: "Home", path: "/" },
    { name: "My submission", path: "/author" },
    { name: "Notification", path: "/author/notifications" },
    { name: "Personal profile", path: "/author/personal-profile" },
    { name: "Logout", path: "/login" },
  ];

  return (
    <div
      className="sidebar-container"
      style={{ width: "250px", height: "100vh", backgroundColor: "#f8f9fa" }}
    >
      <ul
        className="sidebar-menu"
        style={{ listStyle: "none", padding: "20px 0" }}
      >
        {menuItems.map((item, index) => {
          // Kiểm tra xem mục này có đang được chọn không để tô màu
          const isActive =
            location.pathname === item.path ||
            (item.path !== "/" && location.pathname.startsWith(item.path));

          return (
            <li
              key={index}
              className={`menu-item ${isActive ? "active" : ""}`}
              onClick={() => navigate(item.path)}
              style={{
                padding: "15px 25px",
                cursor: "pointer",
                fontSize: "16px",
                transition: "all 0.3s",
                backgroundColor: isActive ? "#e8eaf6" : "transparent", // Màu xanh nhạt khi active
                color: isActive ? "#5865f2" : "#333", // Màu chữ xanh khi active
                borderRadius: "0 25px 25px 0",
                marginBottom: "5px",
                fontWeight: isActive ? "500" : "normal",
              }}
            >
              {item.name}
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default SidebarAuthor;
