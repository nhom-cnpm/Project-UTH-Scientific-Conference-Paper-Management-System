import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../../styles/AuthorStyles.css";

const SubmissionDetailAuthor = () => {
  const navigate = useNavigate();
  const [showMenuId, setShowMenuId] = useState(null);
  const [withdrawId, setWithdrawId] = useState(null);
  const [submissions, setSubmissions] = useState([]);

  // State phục vụ tính năng Undo
  const [undoData, setUndoData] = useState(null);
  const [showUndo, setShowUndo] = useState(false);

  // Hàm tạo thông báo hệ thống
  const createSystemNotification = (message) => {
    const savedNoti =
      JSON.parse(localStorage.getItem("authorNotifications")) || [];
    const newNoti = {
      message: message,
      date:
        new Date().toLocaleDateString() + " " + new Date().toLocaleTimeString(),
    };
    localStorage.setItem(
      "authorNotifications",
      JSON.stringify([newNoti, ...savedNoti]),
    );
  };

  useEffect(() => {
    const savedData = JSON.parse(localStorage.getItem("submissions"));
    if (savedData) {
      setSubmissions(savedData);
    } else {
      const defaultData = [
        {
          id: "P-001",
          title: "Hệ thống giao thông AI",
          topic: "Trí tuệ nhân tạo",
        },
        {
          id: "P-002",
          title: "Xây dựng hệ thống quản lý thư viện thông minh",
          topic: "Trí tuệ nhân tạo",
        },
      ];
      setSubmissions(defaultData);
      localStorage.setItem("submissions", JSON.stringify(defaultData));
    }
  }, []);

  // Hàm xử lý rút bài (Xóa tạm thời)
  const handleWithdraw = () => {
    const paperToDelete = submissions.find((item) => item.id === withdrawId);
    if (!paperToDelete) return;

    setUndoData(paperToDelete);
    setShowUndo(true);

    const updatedData = submissions.filter((item) => item.id !== withdrawId);
    setSubmissions(updatedData);
    localStorage.setItem("submissions", JSON.stringify(updatedData));

    createSystemNotification(
      `You have withdrawn the submission: ${paperToDelete.title}`,
    );

    setWithdrawId(null);
    setShowMenuId(null);

    // Tự động ẩn nút Undo sau 6 giây
    setTimeout(() => {
      setShowUndo(false);
      setUndoData(null);
    }, 6000);
  };

  // Hàm Hoàn tác (Undo)
  const handleUndo = () => {
    if (undoData) {
      const restoredData = [...submissions, undoData];
      setSubmissions(restoredData);
      localStorage.setItem("submissions", JSON.stringify(restoredData));
      createSystemNotification(`Undo successful: Restored "${undoData.title}"`);
      setShowUndo(false);
      setUndoData(null);
    }
  };

  return (
    <div
      className="author-container"
      style={{ position: "relative", padding: "20px" }}
    >
      {/* THANH THÔNG BÁO HOÀN TÁC */}
      {showUndo && (
        <div style={undoSnackbarStyle}>
          <span>You have withdrawn a submission.</span>
          <button onClick={handleUndo} style={undoButtonStyle}>
            UNDO
          </button>
        </div>
      )}

      <h2
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

                {/* ĐẦY ĐỦ 4 NÚT ACTION */}
                {showMenuId === item.id && (
                  <div className="action-menu" style={menuStyle}>
                    <div
                      className="menu-item"
                      style={menuItemStyle}
                      onClick={() =>
                        navigate("/author/edit-submission", {
                          state: { paperData: item },
                        })
                      }
                    >
                      Edit Submission
                    </div>
                    <div
                      className="menu-item"
                      style={{ ...menuItemStyle, color: "#ff4d4d" }}
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
                      style={lastMenuItemStyle}
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

      {/* Modal xác nhận rút bài */}
      {withdrawId && (
        <div style={modalOverlayStyle}>
          <div style={modalContentStyle}>
            <h2 style={{ marginBottom: "40px", fontSize: "20px" }}>
              Are you sure you want to withdraw this post?
            </h2>
            <div
              style={{ display: "flex", justifyContent: "center", gap: "80px" }}
            >
              <button
                onClick={handleWithdraw}
                style={{ ...modalBtnStyle, color: "#ff4d4d" }}
              >
                Yes
              </button>
              <button
                onClick={() => {
                  setWithdrawId(null);
                  setShowMenuId(null);
                }}
                style={{ ...modalBtnStyle, color: "#666" }}
              >
                No
              </button>
            </div>
          </div>
        </div>
      )}

      <button onClick={() => navigate("/author")} style={backBtnStyle}>
        ← Back to My Submissions
      </button>
    </div>
  );
};

// Styles
const undoSnackbarStyle = {
  position: "fixed",
  bottom: "30px",
  left: "50%",
  transform: "translateX(-50%)",
  backgroundColor: "#333",
  color: "white",
  padding: "12px 24px",
  borderRadius: "8px",
  display: "flex",
  alignItems: "center",
  gap: "20px",
  zIndex: 2000,
  boxShadow: "0 4px 15px rgba(0,0,0,0.3)",
};
const undoButtonStyle = {
  backgroundColor: "transparent",
  border: "none",
  color: "#43B5AD",
  fontWeight: "bold",
  cursor: "pointer",
  fontSize: "16px",
};
const menuStyle = {
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
};
const menuItemStyle = {
  padding: "12px 20px",
  cursor: "pointer",
  borderBottom: "1px solid #f5f5f5",
};
const lastMenuItemStyle = { padding: "12px 20px", cursor: "pointer" };
const modalOverlayStyle = {
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
};
const modalContentStyle = {
  backgroundColor: "white",
  padding: "40px",
  borderRadius: "12px",
  textAlign: "center",
  width: "450px",
};
const modalBtnStyle = {
  background: "none",
  border: "none",
  fontSize: "22px",
  fontWeight: "bold",
  cursor: "pointer",
};
const backBtnStyle = {
  marginTop: "30px",
  padding: "10px 20px",
  cursor: "pointer",
  borderRadius: "5px",
  border: "1px solid #ddd",
};

export default SubmissionDetailAuthor;
