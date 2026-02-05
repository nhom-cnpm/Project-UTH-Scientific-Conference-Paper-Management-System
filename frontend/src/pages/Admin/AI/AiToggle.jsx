import React, { useEffect, useState } from "react";
import aiApi from "../../../services/aiApi";

const AiToggle = () => {
  const [enabled, setEnabled] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Gọi hàm getStatus đã được bổ sung trong aiApi.js
    aiApi.getStatus().then((res) => {
      setEnabled(res.enabled);
      setLoading(false);
    });
  }, []);

  const handleToggle = async () => {
    const newStatus = !enabled;
    // Gọi hàm updateStatus thay vì toggleAI
    await aiApi.updateStatus(newStatus);
    setEnabled(newStatus);
  };

  if (loading) return <p>Loading AI status...</p>;

  return (
    <div className="card" style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h2>AI Control</h2>
      <p>Current status: <strong>{enabled ? "Enabled" : "Disabled"}</strong></p>
      <button 
        onClick={handleToggle}
        style={{ backgroundColor: enabled ? "#ff4d4f" : "#52c41a", color: "white", padding: "8px 16px", border: "none", borderRadius: "4px", cursor: "pointer" }}
      >
        {enabled ? "Disable AI" : "Enable AI"}
      </button>
    </div>
  );
};

export default AiToggle;