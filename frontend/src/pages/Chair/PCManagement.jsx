import React, { useState } from "react";

export default function PCManagement() {
  const [list, setList] = useState([
    { name: "Nguyen Van A", email: "a@uth.edu.vn", role: "Reviewer" },
    { name: "Tran Van B", email: "b@uth.edu.vn", role: "Reviewer" },
  ]);

  const [form, setForm] = useState({ name: "", email: "" });

  const addPC = () => {
    setList([...list, { ...form, role: "Reviewer" }]);
    setForm({ name: "", email: "" });
  };

  return (
    <div className="chair-card">
      <h2>Program Committee Management</h2>

      <div className="pc-form">
        <input
          placeholder="Name"
          value={form.name}
          onChange={e => setForm({ ...form, name: e.target.value })}
        />

        <input
          placeholder="Email"
          value={form.email}
          onChange={e => setForm({ ...form, email: e.target.value })}
        />

        <button className="btn-add" onClick={addPC}>
          + Add PC
        </button>
      </div>

      <table className="chair-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
          </tr>
        </thead>

        <tbody>
          {list.map((p, i) => (
            <tr key={i}>
              <td>{p.name}</td>
              <td>{p.email}</td>
              <td>{p.role}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
