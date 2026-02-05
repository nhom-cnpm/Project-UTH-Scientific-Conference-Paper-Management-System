// Giả lập cơ sở dữ liệu tạm thời để đồng bộ trạng thái giữa các Component
let mockAiStatus = {
  enabled: true,
  totalRequests: 1240,
  description: "AI is used for paper review suggestion",
};

const delay = (data, time = 500) =>
  new Promise((resolve) => setTimeout(() => resolve(data), time));

const aiApi = {
  // Lấy trạng thái bật/tắt hiện tại
  getStatus() {
    return delay({ enabled: mockAiStatus.enabled });
  },

  // Lấy toàn bộ thông tin tổng quan
  getOverview() {
    return delay({ ...mockAiStatus });
  },

  // Cập nhật trạng thái bật/tắt
  updateStatus(enabled) {
    mockAiStatus.enabled = enabled; // Cập nhật vào "DB" giả lập
    return delay({ success: true, enabled: mockAiStatus.enabled });
  },

  // Lấy danh sách lịch sử
  getLogs() {
    return delay([
      { id: 1, time: "2026-02-03 09:00", action: "AI enabled", user: "admin" },
      { id: 2, time: "2026-02-03 10:15", action: "AI analyzed paper #23", user: "system" },
      { id: 3, time: "2026-02-05 08:30", action: "AI check plagiarism #45", user: "system" },
    ]);
  },
};

export default aiApi;