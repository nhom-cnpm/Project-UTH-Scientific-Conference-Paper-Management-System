import React from "react";
import Sidebar from "../components/Sidebar";
import MySubmission from "../pages/MySubmission";

const MainLayout = () => {
  return (
    <div
      style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}
    >
      {/* Top Header màu xanh Teal */}
      <div
        style={{
          backgroundColor: "#4db6ac",
          color: "white",
          padding: "10px 20px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h2 style={{ margin: 0, fontSize: "18px" }}>UTH - COMFMS</h2>
        <div style={{ display: "flex", alignItems: "center" }}>
          <div
            style={{
              width: "32px",
              height: "32px",
              borderRadius: "50%",
              backgroundColor: "#eee",
              marginRight: "10px",
            }}
          ></div>
          <span>Nguyen Van A ▼</span>
        </div>
      </div>

      {/* Body: Sidebar + Content */}
      <div style={{ display: "flex", flex: 1 }}>
        <Sidebar />
        <MySubmission />
      </div>
    </div>
  );
};

export default MainLayout;
