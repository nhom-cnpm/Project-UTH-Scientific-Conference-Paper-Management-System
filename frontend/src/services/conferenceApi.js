let conferences = [
  {
    id: 1,
    name: "AI Conference 2026",
    shortName: "AIC2026",
    location: "TP. Hồ Chí Minh",
    startDate: "2026-03-10",
    endDate: "2026-03-12",
    description: "International AI conference",
  },
];

const delay = (data) => new Promise((resolve) => setTimeout(() => resolve(data), 500));

export const conferenceApi = {
  getAll: () => delay([...conferences]),
  
  getConferenceById: (id) => {
    const conf = conferences.find((c) => c.id === Number(id));
    return delay(conf);
  },

  createConference: (payload) => {
    const newConf = { id: Date.now(), ...payload };
    conferences.push(newConf);
    return delay({ success: true });
  },

  updateConference: (id, payload) => {
    conferences = conferences.map((c) =>
      c.id === Number(id) ? { ...c, ...payload } : c
    );
    return delay({ success: true });
  },

  deleteConference: (id) => {
    conferences = conferences.filter((c) => c.id !== Number(id));
    return delay({ success: true });
  }
};