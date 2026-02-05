import React, { useState } from "react";

export default function AssignPapers() {
  const [papers] = useState([
    { title: "AI in Transport", status: "pending" },
    { title: "Blockchain", status: "reviewing" },
  ]);

  const assign = (p) => {
    alert("Assign reviewers for: " + p.title);
  };

  return (
    <div className="chair-card">
      <h2>Assign Papers</h2>

      <input className="search" placeholder="Reviewer name" />

      <table className="chair-table">
        <thead>
          <tr>
            <th>Paper</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {papers.map((p, i) => (
            <tr key={i}>
              <td>{p.title}</td>
              <td>{p.status}</td>
              <td>
                <button className="btn-action" onClick={() => assign(p)}>
                  Assign
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
