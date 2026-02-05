import React from "react";
import "../styles/SidebarAuthor.css"; // Đảm bảo đường dẫn này đúng với cấu trúc của bạn

const SidebarGuest = ({ activePage }) => {
  const menuItems = [
    { name: "Home" },
    { name: "My submission" },
    { name: "Notification" },
    { name: "Personal profile" },
    { name: "Logout" },
  ];

  return (
    <div className="sidebar-container">
      <ul className="sidebar-menu">
        {menuItems.map((item, index) => (
          <li
            key={index}
            className={`menu-item ${item.name === activePage ? "active" : ""}`}
          >
            {item.name}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SidebarGuest;
