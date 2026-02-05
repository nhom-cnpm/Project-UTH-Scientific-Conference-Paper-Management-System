import React from "react";
import { Outlet, useNavigate, useLocation } from "react-router-dom";

const AuthorLayout = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // Logic kiểm tra trang hiện tại để tô màu menu
  const isMySubmission =
    location.pathname === "/author" || location.pathname.includes("submission");
  const isProfile =
    location.pathname.includes("personal-profile") ||
    location.pathname.includes("edit-profile");

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        fontFamily: "Arial, sans-serif",
      }}
    >
      {/* THANH TOPBAR XANH NGỌC */}
      <div
        style={{
          backgroundColor: "#43B5AD",
          color: "white",
          padding: "12px 20px",
          fontWeight: "bold",
          fontSize: "19px",
        }}
      >
        UTH - COMFMS
      </div>

      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
        {/* SIDEBAR */}
        <aside
          style={{
            width: "240px",
            backgroundColor: "#f0f9f9",
            display: "flex",
            flexDirection: "column",
            paddingTop: "20px",
          }}
        >
          <div style={navItemStyle} onClick={() => navigate("/")}>
            Home
          </div>

          {/* MY SUBMISSION */}
          <div
            style={{
              ...navItemStyle,
              backgroundColor: isMySubmission ? "#e0e7ff" : "transparent",
              color: isMySubmission ? "#4f46e5" : "#333",
              borderRadius: "0 20px 20px 0",
              width: "85%",
              fontWeight: isMySubmission ? "bold" : "normal",
            }}
            onClick={() => navigate("/author")}
          >
            My submission
          </div>

          <div style={navItemStyle}>Notification</div>

          {/* PERSONAL PROFILE - ĐÃ THÊM LOGIC BẤM ĐƯỢC */}
          <div
            style={{
              ...navItemStyle,
              backgroundColor: isProfile ? "#e0e7ff" : "transparent",
              color: isProfile ? "#4f46e5" : "#333",
              borderRadius: "0 20px 20px 0",
              width: "85%",
              fontWeight: isProfile ? "bold" : "normal",
            }}
            onClick={() => navigate("/author/personal-profile")} // THÊM DÒNG NÀY
          >
            Personal profile
          </div>

          <div
            style={{ ...navItemStyle, color: "#333", marginTop: "10px" }}
            onClick={() => navigate("/login")}
          >
            Logout
          </div>
        </aside>

        <main style={{ flex: 1, backgroundColor: "#fff", overflowY: "auto" }}>
          <header
            style={{
              display: "flex",
              justifyContent: "flex-end",
              padding: "10px 30px",
              alignItems: "center",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <div
                style={{
                  width: "35px",
                  height: "35px",
                  backgroundColor: "#43B5AD",
                  borderRadius: "50%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "white",
                }}
              >
                👤
              </div>
              <span style={{ fontWeight: "500" }}>Author ▼</span>
            </div>
          </header>
          <div style={{ padding: "0 40px" }}>
            <Outlet /> {/* Nơi hiển thị PersonalProfile.jsx */}
          </div>
        </main>
      </div>
    </div>
  );
};

const navItemStyle = {
  padding: "12px 25px",
  cursor: "pointer",
  fontSize: "15px",
  color: "#333",
};
export default AuthorLayout;
