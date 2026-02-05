import React, { useEffect, useState } from "react";
import systemApi from "../../../services/systemApi";

const AuditLogs = () => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    systemApi.getAuditLogs().then(setLogs);
  }, []);

  return (
    <div>
      <h3>Audit Logs</h3>

      <table>
        <thead>
          <tr>
            <th>Time</th>
            <th>User</th>
            <th>Action</th>
            <th>IP</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((l) => (
            <tr key={l.id}>
              <td>{l.time}</td>
              <td>{l.user}</td>
              <td>{l.action}</td>
              <td>{l.ip}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AuditLogs;
