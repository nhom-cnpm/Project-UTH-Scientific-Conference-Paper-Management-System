import React, { useEffect, useState } from "react";
import aiApi from "../../../services/aiApi";

const AiLogs = () => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    aiApi.getLogs().then((res) => {
      setLogs(res);
    });
  }, []);

  return (
    <div className="card" style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px', marginTop: '20px' }}>
      <h2>AI Logs</h2>
      {logs.length === 0 ? (
        <p>No logs found</p>
      ) : (
        <table className="table" style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#f5f5f5' }}>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>#</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Action</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>User</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Time</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log, index) => (
              <tr key={log.id}>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{index + 1}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{log.action}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{log.user}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{log.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default AiLogs;