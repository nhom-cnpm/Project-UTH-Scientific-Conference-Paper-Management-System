import React from "react";
import { useParams, useNavigate } from "react-router-dom";

const ViewDecision = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  return (
    <div style={{ padding: "20px", maxWidth: "1000px", margin: "0 auto" }}>
      {/* Nút quay lại */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          marginBottom: "20px",
          cursor: "pointer",
          color: "#666",
        }}
        onClick={() => navigate(-1)}
      >
        <span style={{ fontSize: "24px", marginRight: "10px" }}>←</span>
        <span style={{ fontSize: "24px" }}>→</span>
      </div>

      <h2
        style={{ textAlign: "center", marginBottom: "10px", fontSize: "24px" }}
      >
        View Decision
      </h2>

      {/* Nhãn Accept phía trên */}
      <div style={{ marginBottom: "10px" }}>
        <span
          style={{
            backgroundColor: "#5dfc3a",
            padding: "8px 30px",
            borderRadius: "4px",
            fontWeight: "bold",
            display: "inline-block",
          }}
        >
          Accept
        </span>
      </div>

      <p style={{ marginBottom: "20px", fontSize: "16px" }}>
        The paper has been accepted! Below is the decision summary
      </p>

      {/* Khung Decision Summary */}
      <div
        style={{
          border: "1px solid #ddd",
          borderRadius: "4px",
          padding: "25px",
          backgroundColor: "white",
        }}
      >
        <h3 style={{ marginTop: 0, marginBottom: "25px", fontSize: "20px" }}>
          Decision Summary
        </h3>

        {/* Dòng trạng thái và ngày tháng */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "30px",
          }}
        >
          <div style={{ display: "flex", alignItems: "center" }}>
            <span style={{ marginRight: "20px", fontSize: "18px" }}>
              Final Decision
            </span>
            <span
              style={{
                backgroundColor: "#5dfc3a",
                padding: "8px 40px",
                borderRadius: "4px",
                fontWeight: "bold",
              }}
            >
              Accept
            </span>
          </div>
          <div style={{ fontSize: "18px" }}>Decision Date 25/01/2026</div>
        </div>

        {/* Nội dung chi tiết - Khung xám */}
        <div
          style={{
            backgroundColor: "#f8f9fa",
            padding: "30px",
            borderRadius: "4px",
            lineHeight: "1.6",
            fontSize: "16px",
            color: "#333",
            textAlign: "justify",
          }}
        >
          Your pape has been accepted for the conference after peer review. The
          reviewers have provided positive feedback, highlighting the innovative
          approach and solid experimental results. Please carefully address the
          minor revisions suggested in the review comments to enhance the paper
          before the final camera-ready submission desdline.
        </div>
      </div>
    </div>
  );
};

export default ViewDecision;
