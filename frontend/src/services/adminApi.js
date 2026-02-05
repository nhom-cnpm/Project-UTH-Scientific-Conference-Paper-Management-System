// src/api/adminApi.js

// ===== MOCK DATA =====
let users = Array.from({ length: 25 }, (_, i) => ({
  id: i + 1,
  name: `Nguyen Van ${String.fromCharCode(65 + i)}`,
  email: `user${i + 1}@ut.edu.vn`,
  tenant: i < 12 ? "Tenant A" : "Tenant B",
  role: i % 3 === 0 ? "Admin" : i % 3 === 1 ? "Reviewer" : "Student",
  status: i % 2 === 0 ? "online" : "offline",
}));

// ===== UTILS =====
const delay = (data, time = 500) =>
  new Promise((resolve) => setTimeout(() => resolve(data), time));

// ===== ADMIN API =====
export const adminApi = {
  // Lấy danh sách user (có phân trang)
  getUsers({ page = 1, limit = 10 } = {}) {
    const start = (page - 1) * limit;
    const end = start + limit;

    return delay({
      data: users.slice(start, end),
      total: users.length,
      page,
      limit,
    });
  },

  // Lấy chi tiết user
  getUserById(id) {
    const user = users.find((u) => u.id === Number(id));
    return delay(user);
  },

  // Tạo user mới
  createUser(payload) {
    const newUser = {
      id: Date.now(),
      status: "offline",
      ...payload,
    };
    users.push(newUser);
    return delay({ success: true, data: newUser });
  },

  // Cập nhật user
  updateUser(id, payload) {
    users = users.map((u) =>
      u.id === Number(id) ? { ...u, ...payload } : u
    );
    return delay({ success: true });
  },

  // Xóa user
  deleteUser(id) {
    users = users.filter((u) => u.id !== Number(id));
    return delay({ success: true });
  },

  // Đổi role / tenant
  updateUserRole(id, role, tenant) {
    users = users.map((u) =>
      u.id === Number(id) ? { ...u, role, tenant } : u
    );
    return delay({ success: true });
  },
};
