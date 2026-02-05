// src/services/systemApi.js

const delay = (data, time = 500) =>
  new Promise((resolve) => setTimeout(() => resolve(data), time));

// Dữ liệu mẫu cho Nhật ký hệ thống
let auditLogs = [
  { id: 1, time: "2026-02-05 08:30", user: "admin", action: "Login", ip: "192.168.1.1" },
  { id: 2, time: "2026-02-05 09:15", user: "admin", action: "Update Conference #1", ip: "192.168.1.1" },
];

const systemApi = {
  // Lấy nhật ký hệ thống
  getAuditLogs() {
    return delay([...auditLogs]);
  },

  // Lưu cấu hình SMTP
  saveSmtpConfig(payload) {
    console.log("Saving SMTP:", payload);
    return delay({ success: true });
  },

  // Lưu định mức Email
  saveEmailQuota(payload) {
    console.log("Saving Quota:", payload);
    return delay({ success: true });
  },

  // Sao lưu hệ thống
  backupSystem() {
    return delay({ success: true, downloadUrl: "#" });
  },

  // Khôi phục hệ thống
  restoreSystem(file) {
    console.log("Restoring from file:", file.name);
    return delay({ success: true });
  },
};

export default systemApi;