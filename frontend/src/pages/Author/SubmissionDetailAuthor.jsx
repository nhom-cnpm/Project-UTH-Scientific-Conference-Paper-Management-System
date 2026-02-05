import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../../styles/AuthorStyles.css";

const SubmissionDetailAuthor = () => {
  const navigate = useNavigate();
  const [showMenuId, setShowMenuId] = useState(null);

  // NOTE 1: Quản lý danh sách bài viết bằng State để có thể xóa
  const [submissions, setSubmissions] = useState([
    { id: 1, title: "Hệ thống giao thông AI", topic: "Trí tuệ nhân tạo" },
    {
      id: 2,
      title: "Xây dựng hệ thống quản lý thư viện thông minh",
      topic: "Trí tuệ nhân tạo",
    },
  ]);

  // NOTE 2: State quản lý hiển thị Modal xác nhận rút bài
  const [withdrawId, setWithdrawId] = useState(null);

  const handleWithdraw = () => {
    // Xóa bài viết khỏi danh sách
    setSubmissions(submissions.filter((item) => item.id !== withdrawId));
    setWithdrawId(null);
    setShowMenuId(null);
  };

  return (
    <div className="author-container" style={{ position: "relative" }}>
      <h2
        className="author-title"
        style={{ textAlign: "center", marginTop: "20px" }}
      >
        Submission Detail
      </h2>

      <table className="submissions-table">
        <thead style={{ backgroundColor: "#43B5AD", color: "white" }}>
          <tr>
            <th style={{ width: "65%", padding: "15px" }}>
              Title of the article
            </th>
            <th style={{ padding: "15px" }}>Topic</th>
          </tr>
        </thead>
        <tbody>
          {submissions.map((item, index) => (
            <tr key={item.id}>
              <td style={{ padding: "15px" }}>
                {index + 1}. {item.title}
              </td>
              <td
                style={{
                  textAlign: "center",
                  position: "relative",
                  padding: "15px",
                }}
              >
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

                {/* Menu Action */}
                {showMenuId === item.id && (
                  <div
                    className="action-menu"
                    style={{
                      position: "absolute",
                      zIndex: 100,
                      right: 0,
                      backgroundColor: "white",
                      border: "1px solid #ddd",
                      borderRadius: "4px",
                      boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
                    }}
                  >
                    <div
                      className="menu-item"
                      style={{ padding: "10px 20px", cursor: "pointer" }}
                      onClick={() => navigate("/author/edit-submission")}
                    >
                      Edit Submission
                    </div>
                    {/* Sửa tại đây: Mở modal xác nhận khi bấm Withdraw */}
                    <div
                      className="menu-item"
                      style={{ padding: "10px 20px", cursor: "pointer" }}
                      onClick={() => setWithdrawId(item.id)}
                    >
                      Withdraw Submission
                    </div>
                    <div
                      className="menu-item"
                      style={{ padding: "10px 20px" }}
                      onClick={() =>
                        navigate(`/author/view-reviewer/${item.id}`)
                      }
                    >
                      View Reviewer
                    </div>
                    <div
                      className="menu-item"
                      style={{ padding: "10px 20px" }}
                      onClick={() =>
                        navigate(`/author/view-decision/${item.id}`)
                      }
                    >
                      View Decision
                    </div>
                  </div>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* MODAL XÁC NHẬN RÚT BÀI (Withdraw Confirmation) */}
      {withdrawId && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(0,0,0,0.1)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1000,
          }}
        >
          <div
            style={{
              backgroundColor: "white",
              padding: "40px",
              borderRadius: "8px",
              boxShadow: "0 4px 20px rgba(0,0,0,0.2)",
              textAlign: "center",
              width: "550px",
            }}
          >
            <h2 style={{ marginBottom: "50px", fontSize: "24px" }}>
              Are you sure you want to withdraw the submitted post?
            </h2>
            <div style={{ display: "flex", justifyContent: "space-around" }}>
              <button
                onClick={handleWithdraw}
                style={{
                  background: "none",
                  border: "none",
                  fontSize: "24px",
                  fontWeight: "bold",
                  cursor: "pointer",
                }}
              >
                Yes
              </button>
              <button
                onClick={() => setWithdrawId(null)}
                style={{
                  background: "none",
                  border: "none",
                  fontSize: "24px",
                  fontWeight: "bold",
                  cursor: "pointer",
                }}
              >
                No
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SubmissionDetailAuthor;
