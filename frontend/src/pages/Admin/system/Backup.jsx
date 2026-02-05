import React from "react";
import systemApi from "../../../services/systemApi";

const Backup = () => {
  const handleBackup = () => {
    systemApi.backupSystem().then(() => {
      alert("Backup completed");
    });
  };

  return (
    <div>
      <h3>System Backup</h3>
      <button onClick={handleBackup}>Backup Now</button>
    </div>
  );
};

export default Backup;
