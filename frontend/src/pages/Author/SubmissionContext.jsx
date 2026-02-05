import React, { createContext, useState, useContext } from "react";

const SubmissionContext = createContext();

export const SubmissionProvider = ({ children }) => {
  const [submissions, setSubmissions] = useState([
    { id: 1, title: "Hệ thống giao thông AI", topic: "Trí tuệ nhân tạo" },
    {
      id: 2,
      title: "Xây dựng hệ thống quản lý thư viện thông minh",
      topic: "Trí tuệ nhân tạo",
    },
  ]);

  const addSubmission = (newPaper) => {
    setSubmissions([...submissions, { id: Date.now(), ...newPaper }]);
  };

  return (
    <SubmissionContext.Provider value={{ submissions, addSubmission }}>
      {children}
    </SubmissionContext.Provider>
  );
};

export const useSubmissions = () => useContext(SubmissionContext);
