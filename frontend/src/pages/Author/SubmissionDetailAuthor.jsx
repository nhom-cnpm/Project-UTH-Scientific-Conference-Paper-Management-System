import React from "react";
import "../../styles/AuthorStyles.css";

const SubmissionDetailAuthor = () => {
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
      {/* Tiêu đề đổi thành Submission Detail theo ảnh mẫu */}
      <h2 className="author-title" style={{ marginTop: "40px" }}>
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
                {item.topic}
                {/* Thêm dấu ba chấm (...) bên phải Topic như trong ảnh */}
                <span
                  style={{
                    position: "absolute",
                    right: "20px",
                    cursor: "pointer",
                  }}
                >
                  ...
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SubmissionDetailAuthor;
