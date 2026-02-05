import React, { useState } from "react";
import systemApi  from "../../../services/systemApi";

const SmtpConfig = () => {
  const [form, setForm] = useState({
    host: "",
    port: "",
    email: "",
    password: "",
    secure: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm({ ...form, [name]: type === "checkbox" ? checked : value });
  };

  const handleSubmit = () => {
    systemApi.saveSmtpConfig(form).then(() => alert("Saved SMTP config"));
  };

  return (
    <div>
      <h3>SMTP Configuration</h3>

      <input name="host" placeholder="SMTP Host" onChange={handleChange} />
      <input name="port" placeholder="Port" onChange={handleChange} />
      <input name="email" placeholder="Sender Email" onChange={handleChange} />
      <input
        name="password"
        type="password"
        placeholder="Password"
        onChange={handleChange}
      />

      <label>
        <input
          type="checkbox"
          name="secure"
          onChange={handleChange}
        />
        Use SSL/TLS
      </label>

      <button onClick={handleSubmit}>Save</button>
    </div>
  );
};

export default SmtpConfig;
