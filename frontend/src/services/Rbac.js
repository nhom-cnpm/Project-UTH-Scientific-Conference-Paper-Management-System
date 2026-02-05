// src/services/adminApi.js

// ===== MOCK DATA =====
let mockUsers = [
  {
    id: 1,
    name: "Nguyễn Văn A",
    email: "a.nguyen@uth.edu.vn",
    tenant: "Khoa CNTT",
    role: "Admin",
    status: "active",
  },
  {
    id: 2,
    name: "Trần Thị B",
    email: "b.tran@uth.edu.vn",
    tenant: "Khoa Điện - Điện tử",
    role: "Chair",
    status: "active",
  },
  {
    id: 3,
    name: "Lê Văn C",
    email: "c.le@uth.edu.vn",
    tenant: "Khoa Cơ khí",
    role: "Reviewer",
    status: "active",
  },
  {
    id: 4,
    name: "Phạm Thị D",
    email: "d.pham@uth.edu.vn",
    tenant: "Khoa CNTT",
    role: "Student",
    status: "locked",
  },
];

// Giả lập delay API
const delay = (ms = 500) =>
  new Promise((resolve) => setTimeout(resolve, ms));

// ===== API GIẢ =====
export const adminApi = {
  // Lấy danh sách user
  async getUsers() {
    await delay(600);
    return [...mockUsers]; // clone để tránh mutate trực tiếp
  },

  // Cập nhật role user
  async updateUserRole(userId, newRole) {
    await delay(400);

    mockUsers = mockUsers.map((u) =>
      u.id === userId ? { ...u, role: newRole } : u
    );

    return { success: true };
  },

  // (Optional) Khóa / mở user
  async toggleUserStatus(userId) {
    await delay(400);

    mockUsers = mockUsers.map((u) =>
      u.id === userId
        ? { ...u, status: u.status === "active" ? "locked" : "active" }
        : u
    );

    return { success: true };
  },
};
