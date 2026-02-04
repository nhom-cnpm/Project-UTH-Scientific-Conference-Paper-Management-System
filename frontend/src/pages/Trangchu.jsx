import React from "react";
import { Link } from "react-router-dom";
import "../styles/Trangchu.css";

const Home = () => {
  return (
    <div className="landing-container">

      {/* Navbar */}
      <div className="navbar">
        <div className="logo">UTH - COMFMS</div>  

        <div className="nav-links">
          <a href="#">GUIDELINES</a>
          <a href="#">RESULTS</a>
          <a href="#">REGULATIONS</a>

          <Link to="/login" className="btn-login">
            LOGIN
          </Link>
        </div>
      </div>

      {/* Hero */}
      <div className="hero">
        <h1>Empowering Innovation Through</h1>
        <div className="highlight">Scientific Research</div>
        <p className="subtitle">
          The ultimate platform for submitting, managing, and evaluating scientific reports for students and faculty.
        </p>
      </div>

      {/* Events */}
      <div className="events-section">
        <div className="section-header">
          <h2>Ongoing Scientific Events</h2>
          <a href="#" className="view-all">View all →</a>
        </div>

        <div className="event-grid">
          <EventCard
            status="Open"
            badgeClass="open"
            timeLeft="5 days left"
            title="Scientific Research and Innovation"
            desc="Topic: Applying technology to daily life"
            deadline="01/11/2026"
          />

          <EventCard
            status="Upcoming"
            badgeClass="upcoming"
            timeLeft="Starts: Feb 01"
            title="Project Topic 2:"
            desc="Topic: Search and Evaluation Methodologies"
            deadline="02/31/2026"
          />
        </div>
      </div>

      {/* Footer */}
      <div className="footer">
        Ho Chi Minh City University of Transport (UTH)
      </div>

    </div>
  );
};

const EventCard = ({ status, badgeClass, timeLeft, title, desc, deadline }) => (
  <div className="event-card">
    <div className="card-top">
      <span className={`badge ${badgeClass}`}>{status}</span>
      <span className="red-text">⏱ {timeLeft}</span>
    </div>

    <h3 className="card-title">{title}</h3>
    <p className="card-desc">{desc}</p>

    <div className="card-footer">
      <span>Deadline: {deadline}</span>
      <button className="btn-detail">Details</button>
    </div>
  </div>
);

export default Home;