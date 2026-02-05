import React, { useState } from "react";
import "../../styles/AuthorStyles.css";

const SubmissionDetailAuthor = () => {
  const [showMenuId, setShowMenuId] = useState(null);

  const submissions = [
    { id: 1, title: "Hệ thống giao thông AI", topic: "Trí tuệ nhân tạo" },
    {
      id: 2,
      title: "Xây dựng hệ thống quản lý thư viện thông minh",
      topic: "Trí tuệ nhân tạo",
    },
  ];

  return (
    <div className="author-container">
      <h2
        className="author-title"
        style={{ textAlign: "center", marginTop: "20px" }}
      >
        Submission Detail
      </h2>

      <table className="submissions-table">
        <thead>
          <tr>
            <th style={{ width: "65%" }}>Title of the article</th>
            <th>Topic</th>
          </tr>
        </thead>
        <tbody>
          {submissions.map((item, index) => (
            <tr key={item.id}>
              <td>
                {index + 1}. {item.title}
              </td>
              <td style={{ textAlign: "center", position: "relative" }}>
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  {item.topic}
                  <span
                    style={{
                      marginLeft: "10px",
                      cursor: "pointer",
                      fontWeight: "bold",
                    }}
                    onClick={() =>
                      setShowMenuId(showMenuId === item.id ? null : item.id)
                    }
                  >
                    ...
                  </span>
                </div>

                {/* Khung menu nổi tuyệt đối */}
                {showMenuId === item.id && (
                  <div className="action-menu">
                    <div className="menu-item">Edit Submission</div>
                    <div className="menu-item">Withdraw Submission</div>
                    <div className="menu-item">View Reviewer</div>
                    <div className="menu-item">View Decision</div>
                  </div>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SubmissionDetailAuthor;
