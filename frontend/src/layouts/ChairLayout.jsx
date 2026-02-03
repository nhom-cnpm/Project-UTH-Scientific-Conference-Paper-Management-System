import { Link } from "react-router-dom";

export default function ChairLayout({ children }) {
  return (
    <div>
      <h2>Chair Dashboard</h2>
      <nav>
        <Link to="/chair">All Papers</Link>
      </nav>
      <hr />
      {children}
    </div>
  );
}
