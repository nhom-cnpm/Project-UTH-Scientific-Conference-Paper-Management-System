import React, { useState } from "react";

const DeclareCOIDetailsReviewer = ({ onBack, onSubmitSuccess }) => {
  const [isFinalModalOpen, setIsFinalModalOpen] = useState(false);

  const coiTypes = [
    "Same affiliation as the authors",
    "Recent collaboration with the authors",
    "Personal relationship",
    "Financial interest",
    "Other:",
  ];

  // --- CÁC STYLE THUẦN CSS ---
  const containerStyle = {
    maxWidth: "800px",
    margin: "0 auto",
    position: "relative",
    padding: "20px",
    fontFamily: "sans-serif",
    color: "#000",
  };

  const titleStyle = {
    textAlign: "center",
    fontSize: "24px",
    fontWeight: "bold",
    marginBottom: "50px",
    textTransform: "none", // Chỉnh lại theo thiết kế
    color: "#000",
  };

  const sectionTitleStyle = {
    fontSize: "20px",
    fontWeight: "bold",
    marginBottom: "20px",
  };

  const optionContainerStyle = {
    display: "flex",
    alignItems: "center",
    gap: "15px",
    marginBottom: "20px",
    marginLeft: "40px",
  };

  const radioStyle = {
    width: "18px",
    height: "18px",
    cursor: "pointer",
  };

  const textareaStyle = {
    width: "100%",
    border: "1px solid #ccc",
    padding: "15px",
    borderRadius: "4px",
    height: "130px",
    fontSize: "16px",
    outline: "none",
    marginTop: "10px",
  };

  const submitBtnStyle = {
    backgroundColor: "#FF5F5F",
    color: "white",
    padding: "10px 60px",
    borderRadius: "10px",
    border: "none",
    fontWeight: "bold",
    fontSize: "18px",
    cursor: "pointer",
    boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
  };

  return (
    <div style={containerStyle}>
      {/* Nút Back để quay lại Review Action */}
      <button
        onClick={onBack}
        style={{
          background: "none",
          border: "none",
          color: "#4338ca",
          cursor: "pointer",
          fontWeight: "bold",
          fontSize: "16px",
          marginBottom: "20px",
        }}
      >
        ← Back
      </button>

      <h2 style={titleStyle}>Declare COI – Details</h2>

      <div style={{ marginLeft: "40px" }}>
        <h3 style={sectionTitleStyle}>Type of Conflict of Interest:</h3>

        {coiTypes.map((type) => (
          <div key={type} style={optionContainerStyle}>
            <input type="radio" name="coiType" id={type} style={radioStyle} />
            <label
              htmlFor={type}
              style={{ fontSize: "18px", cursor: "pointer" }}
            >
              {type}
            </label>
          </div>
        ))}

        <div style={{ paddingRight: "40px", marginLeft: "33px" }}>
          <textarea
            placeholder="Write details"
            style={textareaStyle}
          ></textarea>
        </div>
      </div>

      <div style={{ textAlign: "center", marginTop: "50px" }}>
        <button
          onClick={() => setIsFinalModalOpen(true)} // Mở modal xác nhận
          style={submitBtnStyle}
        >
          Submit
        </button>
      </div>

      {/* Modal xác nhận - Nhớ truyền onSubmitSuccess vào Modal để quay về trang chính */}
      {isFinalModalOpen && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(0,0,0,0.3)",
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
              borderRadius: "8px",
              maxWidth: "500px",
              textAlign: "center",
            }}
          >
            <h3 style={{ marginBottom: "30px", fontSize: "20px" }}>
              Are you sure you want to submit this COI declaration?
            </h3>
            <div style={{ display: "flex", justifyContent: "space-around" }}>
              <button
                onClick={onSubmitSuccess}
                style={{
                  border: "none",
                  background: "#c4ffc4",
                  fontWeight: "bold",
                  fontSize: "18px",
                  cursor: "pointer",
                  color: "#000",
                }}
              >
                Sure
              </button>
              <button
                onClick={() => setIsFinalModalOpen(false)}
                style={{
                  border: "#000",
                  background: "#ff4b4b",
                  fontWeight: "bold",
                  fontSize: "18px",
                  cursor: "pointer",
                  color: "#000",
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

export default DeclareCOIDetailsReviewer;
