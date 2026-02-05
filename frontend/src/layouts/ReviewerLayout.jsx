import React from "react";
import { Outlet, Link, useLocation } from "react-router-dom";

const ReviewerLayout = () => {
  const location = useLocation();

  const getNavItemStyle = (path) => ({
    padding: "10px 35px",
    textDecoration: "none",
    color:
      location.pathname === path ||
      (path !== "/" && location.pathname.includes(path))
        ? "#4338ca"
        : "#475569",
    backgroundColor:
      location.pathname === path ||
      (path !== "/" && location.pathname.includes(path))
        ? "#e0e7ff"
        : "transparent",
    fontWeight:
      location.pathname === path ||
      (path !== "/" && location.pathname.includes(path))
        ? "bold"
        : "normal",
    borderRadius: "0 25px 25px 0",
    marginRight: "15px",
    display: "block",
    fontSize: "14px",
    transition: "0.3s",
  });

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        width: "100vw",
        margin: 0,
        padding: 0,
        overflow: "hidden",
        backgroundColor: "#f9fbfb",
      }}
    >
      {/* Header gọn gàng */}
      <header
        style={{
          backgroundColor: "#43B5AD",
          color: "white",
          height: "50px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "0 25px",
          flexShrink: 0,
        }}
      >
        <span style={{ fontSize: "18px", fontWeight: "bold" }}>
          UTH - COMFMS
        </span>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          {/* Sửa lại icon User: Nền tròn xanh Teal đậm, Icon trắng */}
          <div
            style={{
              width: "30px",
              height: "30px",
              backgroundColor: "#008080",
              borderRadius: "50%",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
            </svg>
          </div>
          <span style={{ fontSize: "14px" }}>Reviewer ▼</span>
        </div>
      </header>

      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
        <aside
          style={{
            width: "220px",
            backgroundColor: "#f8fafc",
            borderRight: "1px solid #e2e8f0",
            paddingTop: "30px",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <nav style={{ display: "flex", flexDirection: "column", gap: "5px" }}>
            {/* Đã thêm lại nút Home */}
            <Link to="/" style={getNavItemStyle("/")}>
              Home
            </Link>
            <Link to="/reviewer/dashboard" style={getNavItemStyle("dashboard")}>
              Dashboard
            </Link>
            <Link to="/reviewer/assigned" style={getNavItemStyle("assigned")}>
              Assigned Papers
            </Link>

            <Link
              to="/login"
              style={{
                padding: "10px 35px",
                textDecoration: "none",
                color: "#475569",
                fontSize: "14px",
                marginTop: "10px",
              }}
            >
              Logout
            </Link>
          </nav>
        </aside>

        <main style={{ flex: 1, padding: "25px", overflowY: "auto" }}>
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default ReviewerLayout;
