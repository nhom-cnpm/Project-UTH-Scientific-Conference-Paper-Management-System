import React from 'react';
import { Outlet, Link } from 'react-router-dom';

const ReviewerLayout = () => {
  return (
    <div className="reviewer-layout">
      <header style={{ padding: '1rem', background: '#2c3e50', color: 'white' }}>
        <h2>Reviewer Dashboard</h2>
        <nav>
          <Link to="/reviewer/papers" style={{ color: 'white', marginRight: '15px' }}>My Papers</Link>
          <Link to="/login" style={{ color: 'white' }}>Logout</Link>
        </nav>
      </header>
      
      <main style={{ padding: '20px' }}>
        {/* Outlet là nơi nội dung của ReviewerPaperList sẽ hiển thị */}
        <Outlet />
      </main>
    </div>
  );
};

export default ReviewerLayout;