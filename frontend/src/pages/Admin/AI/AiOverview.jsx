import React, { useEffect, useState } from "react";
import aiApi from "../../../services/aiApi";

const AiOverview = () => {
  const [overview, setOverview] = useState(null);

  useEffect(() => {
    aiApi.getOverview().then((res) => {
      setOverview(res);
    });
  }, []);

  if (!overview) return <p>Loading AI overview...</p>;

  return (
    <div className="card" style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px', marginTop: '20px' }}>
      <h2>AI Overview</h2>
      <p><strong>Status:</strong> {overview.enabled ? "Enabled" : "Disabled"}</p>
      <p><strong>Total requests:</strong> {overview.totalRequests}</p>
      <p><strong>Description:</strong> {overview.description}</p>
    </div>
  );
};

export default AiOverview;