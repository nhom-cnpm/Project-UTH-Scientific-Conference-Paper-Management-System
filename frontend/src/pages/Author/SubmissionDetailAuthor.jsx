
// import React, { useState } from "react";

import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../../styles/AuthorStyles.css";


const SubmissionDetailAuthor = () => {
  const navigate = useNavigate();
  const [showMenuId, setShowMenuId] = useState(null);
  const [withdrawId, setWithdrawId] = useState(null);

  // Lấy dữ liệu thực tế từ localStorage khi trang load
  const [submissions, setSubmissions] = useState([]);

  useEffect(() => {
    const savedData = JSON.parse(localStorage.getItem("submissions"));
    if (savedData) {
      setSubmissions(savedData);
    } else {
      // Dữ liệu mặc định nếu chưa có gì trong máy
      const defaultData = [
        { id: 1, title: "Hệ thống giao thông AI", topic: "Trí tuệ nhân tạo" },
        {
          id: 2,
          title: "Xây dựng hệ thống quản lý thư viện thông minh",
          topic: "Trí tuệ nhân tạo",
        },
      ];
      setSubmissions(defaultData);
      localStorage.setItem("submissions", JSON.stringify(defaultData));
    }
  }, []);

  // Hàm xử lý rút bài (Xóa bài)
  const handleWithdraw = () => {
    // 1. Lọc bỏ bài viết có ID trùng với withdrawId
    const updatedData = submissions.filter((item) => item.id !== withdrawId);

    // 2. Cập nhật State để giao diện thay đổi ngay lập tức
    setSubmissions(updatedData);

    // 3. Cập nhật localStorage để đồng bộ với trang "My Submissions"
    localStorage.setItem("submissions", JSON.stringify(updatedData));

    // 4. Đóng Modal và Menu
    setWithdrawId(null);
    setShowMenuId(null);
  };


  // const [submissions, setSubmissions] = useState([]);
  // const [loading, setLoading] = useState(true);

  // useEffect(() => {
  //   fetch("http://localhost:8000/submission/accepted/")
  //     .then((res) => res.json())
  //     .then((data) => {
  //       console.log("API data:", data);
  //       setSubmissions(data);
  //       setLoading(false);
  //     })
  //     .catch((err) => {
  //       console.error("API error:", err);
  //       setLoading(false);
  //     });
  // }, []);


  return (
    <div
      className="author-container"
      style={{ position: "relative", padding: "20px" }}
    >
      <h2
        className="author-title"
        style={{
          textAlign: "left",
          marginBottom: "30px",
          fontWeight: "500",
          fontSize: "24px",
        }}
      >
        Submission Detail
      </h2>

      <table
        className="submissions-table"
        style={{ width: "100%", borderCollapse: "collapse" }}
      >
        {/* Header với màu xanh ngọc chuẩn thiết kế */}
        <thead>
          <tr style={{ backgroundColor: "#43B5AD", color: "white" }}>
            <th
              style={{
                width: "65%",
                padding: "15px",
                textAlign: "left",
                fontWeight: "normal",
                backgroundColor: "#43B5AD",
              }}
            >
              Title of the article
            </th>
            <th
              style={{
                padding: "15px",
                textAlign: "left",
                fontWeight: "normal",
                backgroundColor: "#43B5AD",
              }}
            >
              Topic
            </th>
          </tr>
        </thead>
        <tbody>
          {submissions.map((item, index) => (
            <tr key={item.id} style={{ borderBottom: "1px solid #eee" }}>
              <td style={{ padding: "15px", border: "1px solid #eee" }}>
                {index + 1}. {item.title}
              </td>
              <td
                style={{
                  padding: "15px",
                  border: "1px solid #eee",
                  textAlign: "center",
                  position: "relative",
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
                      fontSize: "18px",
                    }}
                    onClick={() =>
                      setShowMenuId(showMenuId === item.id ? null : item.id)
                    }
                  >
                    ...
                  </span>
                </div>

                {/* Menu Action xuất hiện khi bấm "..." */}
                {showMenuId === item.id && (
                  <div
                    className="action-menu"
                    style={{
                      position: "absolute",
                      zIndex: 100,
                      right: "10px",
                      top: "40px",
                      backgroundColor: "white",
                      border: "1px solid #ddd",
                      borderRadius: "8px",
                      boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
                      minWidth: "180px",
                      textAlign: "left",
                    }}
                  >
                    <div
                      className="menu-item"
                      style={{
                        padding: "12px 20px",
                        cursor: "pointer",
                        borderBottom: "1px solid #f5f5f5",
                      }}
                      onClick={() =>
                        navigate("/author/edit-submission", {
                          state: { article: item },
                        })
                      }
                    >
                      Edit Submission
                    </div>
                    <div
                      className="menu-item"
                      style={{
                        padding: "12px 20px",
                        cursor: "pointer",
                        color: "#ff4d4d",
                        borderBottom: "1px solid #f5f5f5",
                      }}
                      onClick={() => setWithdrawId(item.id)}
                    >
                      Withdraw Submission
                    </div>
                    <div
                      className="menu-item"
                      style={{
                        padding: "12px 20px",
                        cursor: "pointer",
                        borderBottom: "1px solid #f5f5f5",
                      }}
                      onClick={() =>
                        navigate(`/author/view-reviewer/${item.id}`)
                      }
                    >
                      View Reviewer
                    </div>
                    <div
                      className="menu-item"
                      style={{ padding: "12px 20px", cursor: "pointer" }}
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

      {/* MODAL XÁC NHẬN RÚT BÀI */}
      {withdrawId && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(0,0,0,0.3)",
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
              borderRadius: "12px",
              boxShadow: "0 8px 30px rgba(0,0,0,0.3)",
              textAlign: "center",
              width: "500px",
            }}
          >
            <h2
              style={{
                marginBottom: "40px",
                fontSize: "22px",
                color: "#333",
                lineHeight: "1.5",
              }}
            >
              Are you sure you want to withdraw the submitted post?
            </h2>
            <div
              style={{ display: "flex", justifyContent: "center", gap: "80px" }}
            >
              <button
                onClick={handleWithdraw}
                style={{
                  background: "none",
                  border: "none",
                  fontSize: "24px",
                  fontWeight: "bold",
                  cursor: "pointer",
                  color: "#ff4d4d",
                }}
              >
                Yes
              </button>
              <button
                onClick={() => {
                  setWithdrawId(null);
                  setShowMenuId(null);
                }}
                style={{
                  background: "none",
                  border: "none",
                  fontSize: "24px",
                  fontWeight: "bold",
                  cursor: "pointer",
                  color: "#666",
                }}
              >
                No
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Nút quay lại trang chủ Author */}
      <button
        onClick={() => navigate("/author")}
        style={{
          marginTop: "30px",
          padding: "10px 20px",
          cursor: "pointer",
          borderRadius: "5px",
          border: "1px solid #ddd",
        }}
      >
        ← Back to My Submissions
      </button>
    </div>
  );
};

export default SubmissionDetailAuthor;
