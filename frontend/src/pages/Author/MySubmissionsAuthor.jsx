import React from "react";
import { useNavigate } from "react-router-dom";
import "../../styles/AuthorStyles.css";

const MySubmissionsAuthor = () => {
  const navigate = useNavigate();
  const submissions = [
    {
      id: 1,
      title: "Hệ thống giao thông AI",
      topic: "Trí tuệ nhân tạo",
    },
    {
      id: 2,
      title: "Xây dựng hệ thống quản lý thư viện thông minh",
      topic: "Trí tuệ nhân tạo",
    },
  ];

  return (
    <div className="author-container">
      {/* Nút góc trên bên trái */}
      <button className="btn-submit-new">
        <span style={{ fontSize: "22px" }}>+</span> Submit new articles!
      </button>

      <h2 className="author-title">List of your articles</h2>

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
              <td style={{ textAlign: "center" }}>{item.topic}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Nút to dưới cùng */}
      <button
        className="btn-detail"
        onClick={() => navigate("/author/submission-detail")}
      >
        Submission Detail
      </button>
    </div>
  );
};

export default MySubmissionsAuthor;
