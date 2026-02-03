import React from "react";

const NotificationTable = ({ notifications = [] }) => {
  return (
    <div className="table-container">
      <table className="custom-table">
        <thead>
          <tr>
            <th>Notification name</th>
            <th>Date sent</th>
          </tr>
        </thead>
        <tbody>
          {notifications.length > 0 ? (
            notifications.map((item, index) => (
              <tr key={index}>
                <td>{item.name}</td>
                <td>{item.date}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="2" className="no-data">
                <em>No announcement yet</em>
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default NotificationTable;
