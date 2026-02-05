import React, { useState } from "react";
import systemApi from "../../../services/systemApi";

const Restore = () => {
  const [file, setFile] = useState(null);

  const handleRestore = () => {
    if (!file) {
      alert("Please select backup file");
      return;
    }

    systemApi.restoreSystem(file).then(() => {
      alert("System restored");
    });
  };

  return (
    <div>
      <h3>Restore System</h3>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={handleRestore}>Restore</button>
    </div>
  );
};

export default Restore;
