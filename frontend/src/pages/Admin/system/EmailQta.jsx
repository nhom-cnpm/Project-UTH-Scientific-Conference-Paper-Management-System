import React, { useState } from "react";
import  systemApi from "../../../services/systemApi";

const EmailQuota = () => {
  const [quota, setQuota] = useState({
    daily: "",
    monthly: "",
  });

  const handleSave = () => {
    systemApi.saveEmailQuota(quota).then(() => alert("Quota saved"));
  };

  return (
    <div>
      <h3>Email Quota</h3>

      <input
        placeholder="Daily Limit"
        onChange={(e) =>
          setQuota({ ...quota, daily: e.target.value })
        }
      />

      <input
        placeholder="Monthly Limit"
        onChange={(e) =>
          setQuota({ ...quota, monthly: e.target.value })
        }
      />

      <button onClick={handleSave}>Save</button>
    </div>
  );
};

export default EmailQuota;
