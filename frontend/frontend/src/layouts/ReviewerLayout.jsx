import { Link } from "react-router-dom";

export default function ReviewerLayout({ children }) {
  return (
    <div>
      <h2>Reviewer Dashboard</h2>
      <nav>
        <Link to="/reviewer">Assigned Papers</Link>
      </nav>
      <hr />
      {children}
    </div>
  );
}
