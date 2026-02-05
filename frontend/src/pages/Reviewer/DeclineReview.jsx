import React, { useState } from "react"; // 1. Note: Thêm useState ở đây

const DeclineReview = ({ onBack, onSubmitSuccess }) => {
  // 2. Note: Thêm state quản lý đóng/mở Modal
  const [isModalOpen, setIsModalOpen] = useState(false);

  const containerStyle = {
    padding: "40px",
    backgroundColor: "white",
    borderRadius: "12px",
    maxWidth: "900px",
    margin: "0 auto",
    fontFamily: "sans-serif",
    position: "relative", // Để Modal căn giữa đúng hơn
    color: "#000",
  };

  const optionStyle = {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    marginBottom: "20px",
    fontSize: "18px",
    cursor: "pointer",
  };

  // 3. Note: Tạo giao diện Modal xác nhận
  const renderConfirmModal = () => (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(0,0,0,0.4)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 1000,
      }}
    >
      <div
        style={{
          backgroundColor: "white",
          padding: "40px",
          borderRadius: "12px",
          maxWidth: "550px",
          textAlign: "center",
          boxShadow: "0 4px 20px rgba(0,0,0,0.2)",
        }}
      >
        <h3
          style={{ fontSize: "22px", marginBottom: "40px", lineHeight: "1.4" }}
        >
          After submitting the reasons for rejection, the reviewer will no
          longer be able to consider this paper.
        </h3>
        <div style={{ display: "flex", justifyContent: "space-around" , color: "#000",}}>
          <button
            onClick={onSubmitSuccess}
            style={{
              background: "#c4ffc4",
              border: "#000",
              fontSize: "20px",
              fontWeight: "bold",
              cursor: "pointer",
              color: "#000",
            }}
          >
            Sure
          </button>
          <button
            onClick={() => setIsModalOpen(false)}
            style={{
              background: "#ff4b4b",
              border: "#000",
              fontSize: "20px",
              fontWeight: "bold",
              cursor: "pointer",
              color: "#000",
            }}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div style={containerStyle}>
      <button
        onClick={onBack}
        style={{
          background: "none",
          border: "none",
          color: "#4338ca",
          cursor: "pointer",
          fontWeight: "bold",
          fontSize: "16px",
          display: "flex",
          alignItems: "center",
          marginBottom: "30px",
        }}
      >
        ← Back
      </button>

      <h2
        style={{
          textAlign: "center",
          fontSize: "24px",
          fontWeight: "bold",
          marginBottom: "50px",
        }}
      >
        Decline review
      </h2>

      <div style={{ paddingLeft: "50px" , color: "#000",}}>
        {[
          "Paper Not in My Field",
          "Lack of Expertise",
          "Time Constraints",
          "Conflict of Interest",
          "Other:",
        ].map((reason) => (
          <label key={reason} style={optionStyle}>
            <input
              type="radio"
              name="declineReason"
              style={{ width: "18px", height: "18px", cursor: "pointer" }}
            />
            {reason}
          </label>
        ))}

        <div style={{ marginTop: "10px", paddingRight: "50px" }}>
          <textarea
            placeholder="Write another reason....."
            style={{
              width: "100%",
              height: "150px",
              padding: "15px",
              borderRadius: "4px",
              border: "1px solid #ccc",
              fontSize: "16px",
              outline: "none",
            }}
          />
        </div>
      </div>

      <div style={{ textAlign: "center", marginTop: "40px" }}>
        <button
          onClick={() => setIsModalOpen(true)} // 4. Note: Đổi từ onSubmitSuccess thành mở Modal
          style={{
            backgroundColor: "#FF5F5F",
            color: "white",
            padding: "12px 40px",
            borderRadius: "10px",
            border: "none",
            fontWeight: "bold",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          Submit Reason
        </button>
      </div>

      {/* 5. Note: Hiển thị Modal nếu isModalOpen = true */}
      {isModalOpen && renderConfirmModal()}
    </div>
  );
};

export default DeclineReview;
