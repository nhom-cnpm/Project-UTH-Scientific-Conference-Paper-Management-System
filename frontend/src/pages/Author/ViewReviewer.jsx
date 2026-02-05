import React from "react";
import { useParams, useNavigate } from "react-router-dom";

const ViewReviewer = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  // Giả lập dữ liệu khác nhau tùy theo ID bài viết
  const reviewData = {
    1: {
      reviewers: [
        {
          name: "Reviewer 1",
          score: "4/5",
          recommendation: "Accept",
          date: "25/01/2026",
        },
        {
          name: "Reviewer 2",
          score: "3/5",
          recommendation: "Accept",
          date: "25/01/2026",
        },
      ],
      comment:
        "Overall, this is a well-written paper that address a crucial issue in modern smart cities. I suggest revising Chapters 2 and 4 to make the arguments clearer.",
    },
    2: {
      reviewers: [
        {
          name: "Reviewer 3",
          score: "5/5",
          recommendation: "Strong Accept",
          date: "28/01/2026",
        },
      ],
      comment: "Excellent work! No major changes needed.",
    },
  };

  const currentReview = reviewData[id] || {
    reviewers: [],
    comment: "No feedback yet.",
  };

  return (
    <div style={{ padding: "20px" }}>
      {/* Nút quay lại */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          marginBottom: "20px",
          cursor: "pointer",
        }}
        onClick={() => navigate(-1)}
      >
        <span style={{ fontSize: "20px", marginRight: "10px" }}>←</span>
        <span style={{ fontSize: "20px" }}>→</span>
      </div>

      <h2 style={{ textAlign: "center", marginBottom: "30px" }}>
        View Reviewer
      </h2>
      <p style={{ textAlign: "center", color: "#555", marginBottom: "30px" }}>
        The paper is currently being reviewed. You can view feedback from
        reviewes here
      </p>

      {/* Bảng đánh giá */}
      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          border: "1px solid #ddd",
          marginBottom: "30px",
        }}
      >
        <thead>
          <tr style={{ backgroundColor: "#eee" }}>
            <th
              style={{
                padding: "12px",
                border: "1px solid #ddd",
                textAlign: "left",
              }}
            >
              Reviewer
            </th>
            <th
              style={{
                padding: "12px",
                border: "1px solid #ddd",
                textAlign: "left",
              }}
            >
              Score
            </th>
            <th
              style={{
                padding: "12px",
                border: "1px solid #ddd",
                textAlign: "left",
              }}
            >
              Recommendation
            </th>
            <th
              style={{
                padding: "12px",
                border: "1px solid #ddd",
                textAlign: "left",
              }}
            >
              Submitted On
            </th>
          </tr>
        </thead>
        <tbody>
          {currentReview.reviewers.map((rev, idx) => (
            <tr key={idx}>
              <td style={{ padding: "12px", border: "1px solid #ddd" }}>
                {rev.name}
              </td>
              <td style={{ padding: "12px", border: "1px solid #ddd" }}>
                {rev.score}
              </td>
              <td style={{ padding: "12px", border: "1px solid #ddd" }}>
                {rev.recommendation}
              </td>
              <td style={{ padding: "12px", border: "1px solid #ddd" }}>
                {rev.date}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Phần nhận xét tổng quát */}
      <div>
        <h3 style={{ fontSize: "18px", marginBottom: "15px" }}>
          Overall Comments
        </h3>
        <p
          style={{
            paddingLeft: "30px",
            lineHeight: "1.6",
            color: "#333",
            fontStyle: "normal",
          }}
        >
          {currentReview.comment}
        </p>
      </div>
    </div>
  );
};

export default ViewReviewer;
