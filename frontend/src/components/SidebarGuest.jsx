import React from "react";

const Sidebar = () => {
  const menuItems = [
    { name: "Home", active: false },
    { name: "My submission", active: true }, // Đang chọn mục này
    { name: "Notification", active: false },
    { name: "Personal profile", active: false },
    { name: "Logout", active: false },
  ];

  return (
    <div
      style={{
        width: "250px",
        backgroundColor: "#f0f7f7",
        height: "100vh",
        padding: "20px",
      }}
    >
      <ul style={{ listStyle: "none", padding: 0, marginTop: "50px" }}>
        {menuItems.map((item, index) => (
          <li
            key={index}
            style={{
              padding: "12px 20px",
              marginBottom: "10px",
              borderRadius: "8px",
              cursor: "pointer",
              backgroundColor: item.active ? "#e0e7ff" : "transparent",
              color: item.active ? "#3b82f6" : "#333",
              fontWeight: item.active ? "bold" : "normal",
            }}
          >
            {item.name}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
