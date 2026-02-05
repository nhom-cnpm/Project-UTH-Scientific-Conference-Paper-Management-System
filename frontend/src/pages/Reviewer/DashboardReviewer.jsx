import React from "react";

const DashboardReviewer = () => {
  const cardStyle = {
    flex: 1,
    height: "140px",
    borderRadius: "8px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    color: "white",
    fontSize: "36px",
    fontWeight: "bold",
    position: "relative",
    boxShadow: "0 4px 10px rgba(0,0,0,0.05)",
  };

  const labelStyle = {
    position: "absolute",
    top: "15px",
    fontSize: "15px",
    fontWeight: "normal",
  };

  return (
    <div
      style={{
        backgroundColor: "white",
        padding: "30px",
        borderRadius: "10px",
        border: "1px solid #f0f0f0",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "20px",
        }}
      >
        <h2 style={{ fontSize: "20px", fontWeight: "bold", color: "#333" }}>
          View Assigned Papers
        </h2>
        <span style={{ color: "#1864FF", cursor: "pointer", fontSize: "13px" }}>
          View More ▾
        </span>
      </div>

      <div style={{ display: "flex", gap: "20px" }}>
        <div style={{ ...cardStyle, backgroundColor: "#FF5A5A" }}>
          5<span style={labelStyle}>Assigned Paper</span>
        </div>
        <div style={{ ...cardStyle, backgroundColor: "#FF9F43" }}>
          <span style={labelStyle}>Reviewed</span>2
        </div>
        <div style={{ ...cardStyle, backgroundColor: "#1864FF" }}>
          <span style={labelStyle}>Pending</span>3
        </div>
      </div>
    </div>
  );
};

export default DashboardReviewer;
