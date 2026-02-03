import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import DashboardLayout from "./layouts/DashboardLayout";
import ReviewerLayout from "./layouts/ReviewerLayout";
import ChairLayout from "./layouts/ChairLayout";
import ReviewerPaperList from "./pages/ReviewerPaperList";
import PaperDetail from "./pages/PaperDetail";
import Login from "./pages/Login";
import Trangchu from "./pages/Trangchu";
import TrangcuaQtvien from "./TrangcuaQtvien";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Trangchu />} />
        <Route path="/login" element={<Login />} />

        <Route path="/admin" element={<TrangcuaQtvien />} />

        {/* CHAIR */}
        <Route path="/chair" element={<ChairLayout />} />

        {/* REVIEWER */}
        <Route path="/reviewer" element={<ReviewerLayout />}>
          <Route index element={<ReviewerPaperList />} />
          <Route path="paper/:id" element={<PaperDetail />} />
        </Route>

        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
