import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

/* ===== LAYOUT ===== */
import ReviewerLayout from "./layouts/ReviewerLayout";

/* ===== PUBLIC ===== */
import Trangchu from "./pages/Trangchu";
import Login from "./pages/Login";

/* ===== ADMIN CŨ ===== */
import TrangcuaQtvien from "./pages/TrangcuaQtvien";
import EditUser from "./pages/EditUser";

import MainLayoutReviewer from "./layouts/MainLayoutReviewer";
import DashboardReviewer from "./pages/DashboardReviewer";
import AssignedPapersReviewer from "./pages/AssignedPapersReviewer";
import ReviewActionReviewer from "./pages/ReviewActionReviewer";
import PaperDetailReviewer from "./pages/PaperDetailReviewer";
import SubmitReview from "./pages/SubmitReview";
import DeclineReview from "./pages/DeclineReview";
import DeclareCOIDetailsReviewer from "./pages/DeclareCOIDetailsReviewer";
function App() {
  return (
    <Router>
      <Routes>
        {/* ===== PUBLIC ===== */}
        <Route path="/" element={<Trangchu />} />
        <Route path="/login" element={<Login />} />
        {/* ADMIN */}
        <Route path="/admin" element={<TrangcuaQtvien />} />
        <Route path="/adminPhanquyen" element={<TrangcuaQtvien />} />
        <Route path="/conference-manage" element={<AdminQuanli />} />
        <Route path="/conference-manage/edit" element={<EditUser />} />q
        {/* CHAIR */}
        <Route path="/chair" element={<ChairLayout />} />
        {/* REVIEWER */}
        <Route path="/reviewer" element={<ReviewerLayout />}>
          <Route index element={<ReviewerPaperList />} />
          <Route path="paper/:id" element={<PaperDetail />} />
          <Route path="dashboard" element={<DashboardReviewer />} />
          <Route path="assigned" element={<AssignedPapersReviewer />} />
          <Route path="review" element={<ReviewActionReviewer />} />
          <Route path="paper-detail" element={<PaperDetailReviewer />} />
          <Route path="submit-review" element={<SubmitReview />} />
          <Route path="decline-review" element={<DeclineReview />} />
          <Route
            path="declare-coi-details"
            element={<DeclareCOIDetailsReviewer />}
          />
        </Route>
        {/* FALLBACK */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
