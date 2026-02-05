// services/chairApi.js

// GIẢ LẬP DỮ LIỆU
const fakeDB = {
  conferences: [
    { id: 1, name: "Hội nghị CNTT 2025", deadline: "2025-06-01" },
    { id: 2, name: "AI Research", deadline: "2025-07-15" },
  ],

  pcMembers: [
    { id: 1, name: "Nguyen Van A", role: "Reviewer", email: "a@uth.edu.vn" },
    { id: 2, name: "Tran Van B", role: "Reviewer", email: "b@uth.edu.vn" },
  ],

  papers: [
    { id: 1, title: "AI in Transport", status: "pending" },
    { id: 2, title: "Blockchain", status: "reviewing" },
  ]
};

export const chairApi = {
  getDashboard: () =>
    Promise.resolve({
      totalConf: fakeDB.conferences.length,
      totalPC: fakeDB.pcMembers.length,
      totalPaper: fakeDB.papers.length,
    }),

  getPC: () => Promise.resolve(fakeDB.pcMembers),

  addPC: (pc) => {
    fakeDB.pcMembers.push({ id: Date.now(), ...pc });
    return Promise.resolve(true);
  },

  getPapers: () => Promise.resolve(fakeDB.papers),

  assignPaper: (paperId, reviewer) => {
    return Promise.resolve({ paperId, reviewer });
  },
};
