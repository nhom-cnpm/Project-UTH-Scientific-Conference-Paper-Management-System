import React, { useState, useEffect } from "react";

const NotificationAuthor = () => {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    // Lấy danh sách thông báo từ máy
    const savedNoti =
      JSON.parse(localStorage.getItem("authorNotifications")) || [];
    setNotifications(savedNoti);
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2 style={{ marginBottom: "20px", fontSize: "20px" }}>
        Your notification list
      </h2>

      <div
        style={{
          backgroundColor: "#f9f9f9",
          borderRadius: "8px",
          overflow: "hidden",
          minHeight: "300px",
        }}
      >
        {/* Header bảng thông báo */}
        <div
          style={{
            display: "flex",
            backgroundColor: "#eee",
            padding: "12px",
            fontWeight: "bold",
          }}
        >
          <div style={{ flex: 2, textAlign: "center" }}>Notification name</div>
          <div style={{ flex: 1, textAlign: "center" }}>Date sent</div>
        </div>

        {/* Nội dung thông báo */}
        {notifications.length > 0 ? (
          notifications.map((noti, index) => (
            <div
              key={index}
              style={{
                display: "flex",
                padding: "12px",
                borderBottom: "1px solid #ddd",
              }}
            >
              <div style={{ flex: 2 }}>{noti.message}</div>
              <div style={{ flex: 1, textAlign: "center" }}>{noti.date}</div>
            </div>
          ))
        ) : (
          <div
            style={{
              textAlign: "center",
              padding: "40px",
              fontStyle: "italic",
              color: "#666",
            }}
          >
            No announcement yet
          </div>
        )}
      </div>
    </div>
  );
};

export default NotificationAuthor;
