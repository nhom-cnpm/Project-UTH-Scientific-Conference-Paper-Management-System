import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const EditSubmission = () => {
  const navigate = useNavigate();
  const [showConfirm, setShowConfirm] = useState(false);
  // State mới để hiện thông báo đã replace file
  const [showSuccessMsg, setShowSuccessMsg] = useState(false);

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

  const handleReplacePDF = () => {
    // Giả lập logic replace file thành công
    setShowSuccessMsg(true);
    createSystemNotification(
      "You have successfully replaced the PDF file for Paper",
    );

    // Sau 3 giây thì ẩn thông báo đi
    setTimeout(() => {
      setShowSuccessMsg(false);
    }, 3000);
  };

  const handleSave = () => {
    setShowConfirm(true);
  };

  const confirmSave = () => {
    createSystemNotification(
      "Submission metadata for Paper  has been updated.",
    );
    setShowConfirm(false);
    navigate("/author/submission-detail");
  };

  return (
    <div style={{ padding: "20px", position: "relative" }}>
      {/* THÔNG BÁO THÀNH CÔNG (Hiện phía trên cùng) */}
      {showSuccessMsg && (
        <div
          style={{
            position: "fixed",
            top: "20px",
            right: "20px",
            backgroundColor: "#4caf50",
            color: "white",
            padding: "15px 25px",
            borderRadius: "4px",
            boxShadow: "0 2px 10px rgba(0,0,0,0.2)",
            zIndex: 2000,
            fontWeight: "bold",
          }}
        >
          File PDF đã được replace thành công!
        </div>
      )}

      <h2 style={{ marginBottom: "5px" }}>Edit Submission</h2>
      <p style={{ color: "#666", marginBottom: "25px" }}>
        You can update subission informatiuon before the review process starts
      </p>

      <div
        style={{
          border: "1px solid #ddd",
          borderRadius: "4px",
          opacity: showConfirm ? 0.3 : 1,
        }}
      >
        <div
          style={{
            backgroundColor: "#eee",
            padding: "15px",
            borderBottom: "1px solid #ddd",
          }}
        >
          <div style={{ fontWeight: "bold" }}>Paper ID: P-001</div>
          <div>Submission Date: 10/02/2026</div>
        </div>

        <div style={{ padding: "20px" }}>
          <h3 style={{ fontSize: "18px", marginBottom: "15px" }}>
            Edit Metadata
          </h3>
          {/* ... giữ nguyên phần danh sách thông tin ... */}

          <hr
            style={{
              border: "0",
              borderTop: "1px solid #eee",
              margin: "20px 0",
            }}
          />

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "start",
            }}
          >
            <div>
              <strong>PDF Manage:</strong> current_paper.pdf
              <p
                style={{ color: "#999", fontStyle: "italic", fontSize: "13px" }}
              >
                Uploading a new file will replace the existing PDF
              </p>
            </div>
            {/* SỬA TẠI ĐÂY: Thêm sự kiện onClick cho nút Replace */}
            <button
              onClick={handleReplacePDF}
              style={{
                backgroundColor: "#0052ff",
                color: "white",
                border: "none",
                padding: "8px 20px",
                borderRadius: "4px",
                cursor: "pointer",
              }}
            >
              Replace PDF
            </button>
          </div>
        </div>

        <div
          style={{ display: "flex", justifyContent: "center", padding: "20px" }}
        >
          <button
            onClick={handleSave}
            style={{
              backgroundColor: "red",
              color: "white",
              border: "none",
              padding: "10px 50px",
              borderRadius: "4px",
              fontWeight: "bold",
              cursor: "pointer",
            }}
          >
            Save Changes
          </button>
        </div>
      </div>

      {/* MODAL XÁC NHẬN */}
      {showConfirm && (
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
              width: "500px",
            }}
          >
            <h2 style={{ marginBottom: "40px" }}>
              Are you sure you want to save the changes?
            </h2>
            <div style={{ display: "flex", justifyContent: "space-around" }}>
              <button
                onClick={confirmSave}
                style={{
                  background: "none",
                  border: "none",
                  fontSize: "22px",
                  fontWeight: "bold",
                  cursor: "pointer",
                }}
              >
                Save Changes
              </button>
              <button
                onClick={() => setShowConfirm(false)}
                style={{
                  background: "none",
                  border: "none",
                  fontSize: "22px",
                  fontWeight: "bold",
                  cursor: "pointer",
                }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EditSubmission;
