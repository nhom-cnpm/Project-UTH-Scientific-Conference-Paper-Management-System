import React from "react";
import { useNavigate } from "react-router-dom";

const MySubmissionsAuthor = () => {
  const navigate = useNavigate();

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        width: "100%",
        alignItems: "center",
      }}
    >
      <div style={{ width: "100%", textAlign: "left", marginBottom: "25px" }}>
        <button
          style={{
            backgroundColor: "#5865f2",
            color: "white",
            border: "none",
            padding: "10px 25px",
            borderRadius: "15px",
            cursor: "pointer",
            fontWeight: "500",
          }}
        >
          + Submit new articles!
        </button>
      </div>

      <h2
        style={{
          width: "100%",
          textAlign: "left",
          marginBottom: "20px",
          fontWeight: "500",
          fontSize: "22px",
        }}
      >
        List of your articles
      </h2>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ backgroundColor: "#43B5AD" }}>
            <th
              style={{
                padding: "15px",
                border: "1px solid #ddd",
                textAlign: "left",
                fontWeight: "normal",
                backgroundColor: "#43B5AD", // ÉP MÀU XANH NGỌC Ở ĐÂY
                color: "white",
              }}
            >
              Title of the article
            </th>
            <th
              style={{
                padding: "15px",
                border: "1px solid #ddd",
                textAlign: "left",
                fontWeight: "normal",
                width: "30%",
                backgroundColor: "#43B5AD", // ÉP MÀU XANH NGỌC Ở ĐÂY
                color: "white",
              }}
            >
              Topic
            </th>
          </tr>
        </thead>
        <tbody>
          <tr style={{ borderBottom: "1px solid #eee" }}>
            <td style={{ padding: "15px", border: "1px solid #eee" }}>
              1. Hệ thống giao thông AI
            </td>
            <td style={{ padding: "15px", border: "1px solid #eee" }}>
              Trí tuệ nhân tạo
            </td>
          </tr>
          <tr style={{ borderBottom: "1px solid #eee" }}>
            <td style={{ padding: "15px", border: "1px solid #eee" }}>
              2. Xây dựng hệ thống quản lý thư viện thông minh
            </td>
            <td style={{ padding: "15px", border: "1px solid #eee" }}>
              Trí tuệ nhân tạo
            </td>
          </tr>
        </tbody>
      </table>

      {/* Khung đỏ cam Submission Detail - Giữ nguyên bo tròn và căn giữa */}
      <div
        style={{
          marginTop: "60px",
          width: "100%",
          display: "flex",
          justifyContent: "center",
        }}
      >
        <button
          onClick={() => navigate("/author/submission-detail")}
          style={{
            backgroundColor: "#ff6b6b",
            color: "white",
            border: "none",
            padding: "12px 70px",
            borderRadius: "30px",
            fontSize: "17px",
            fontWeight: "bold",
            cursor: "pointer",
            boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
          }}
        >
          Submission Detail
        </button>
      </div>
    </div>
  );
};

export default MySubmissionsAuthor;
