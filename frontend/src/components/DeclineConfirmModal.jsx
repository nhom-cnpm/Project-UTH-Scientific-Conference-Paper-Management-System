import React from "react";

const DeclineConfirmModal = ({ onSure, onCancel }) => {
  const overlayStyle = {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: "rgba(0, 0, 0, 0.3)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 1000,
  };

  const modalStyle = {
    backgroundColor: "white",
    padding: "40px",
    borderRadius: "8px",
    maxWidth: "500px",
    textAlign: "center",
    boxShadow: "0 4px 15px rgba(0,0,0,0.2)",
  };

  const buttonStyle = {
    background: "none",
    border: "none",
    fontSize: "20px",
    cursor: "pointer",
    fontWeight: "500",
    margin: "0 50px",
  };

  return (
    <div style={overlayStyle}>
      <div style={modalStyle}>
        <h3
          style={{ fontSize: "22px", lineHeight: "1.5", marginBottom: "40px" }}
        >
          After submitting the reasons for rejection, the reviewer will no
          longer be able to consider this paper.
        </h3>
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <button onClick={onSure} style={buttonStyle}>
            Sure
          </button>
          <button onClick={onCancel} style={buttonStyle}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeclineConfirmModal;
