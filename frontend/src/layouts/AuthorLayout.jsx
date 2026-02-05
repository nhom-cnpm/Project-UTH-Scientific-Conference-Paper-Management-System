import React from "react";
import { Outlet, useNavigate } from "react-router-dom";

const AuthorLayout = () => {
  const navigate = useNavigate();
  const username = localStorage.getItem("username") || "Author";

  return (
    <div
      style={{
        display: "flex",
        minHeight: "100vh",
        fontFamily: "Arial, sans-serif",
      }}
    >
      {/* SIDEBAR - Màu xanh nhạt theo ảnh mẫu */}
      <aside
        style={{
          width: "250px",
          backgroundColor: "#f0f9f9",
          borderRight: "1px solid #e0e0e0",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div
          style={{
            padding: "20px",
            color: "#43B5AD",
            fontWeight: "bold",
            fontSize: "18px",
          }}
        >
          UTH - COMFMS
        </div>

        <nav style={{ flex: 1 }}>
          <div style={navItemStyle}>Home</div>
          {/* Mục My submission được highlight màu xanh tím */}
          <div
            style={{
              ...navItemStyle,
              backgroundColor: "#e0e7ff",
              color: "#4f46e5",
              borderRadius: "0 20px 20px 0",
              marginRight: "10px",
            }}
          >
            My submission
          </div>
          <div style={navItemStyle}>Notification</div>
          <div style={navItemStyle}>Personal profile</div>
          <div
            style={{ ...navItemStyle, marginTop: "auto", color: "#666" }}
            onClick={() => {
              localStorage.clear();
              navigate("/login");
            }}
          >
            Logout
          </div>
        </nav>
      </aside>

      {/* CONTENT AREA */}
      <main style={{ flex: 1, backgroundColor: "#fff" }}>
        {/* Header góc trên bên phải */}
        <header
          style={{
            display: "flex",
            justifyContent: "flex-end",
            padding: "15px 30px",
            alignItems: "center",
            borderBottom: "1px solid #f5f5f5",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "10px",
              cursor: "pointer",
            }}
          >
            <div
              style={{
                width: "32px",
                height: "32px",
                backgroundColor: "#43B5AD",
                borderRadius: "50%",
              }}
            ></div>
            <span style={{ fontWeight: "500" }}>{username} ▼</span>
          </div>
        </header>

        {/* Nơi hiển thị nội dung của MySubmissionsAuthor.jsx */}
        <div style={{ padding: "20px" }}>
          <Outlet />
        </div>
      </main>
    </div>
  );
};

const navItemStyle = {
  padding: "12px 25px",
  margin: "5px 0",
  cursor: "pointer",
  fontSize: "15px",
  color: "#333",
  transition: "0.2s",
};

export default AuthorLayout;
