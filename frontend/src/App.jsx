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
import PersonalProfile from "./pages/PersonalProfile";

/* ===== ADMIN MỚI ===== */
import AdminQuanli from "./pages/Admin/AdminQuanli";

/* ===== CONFERENCE ===== */
import CreateConference from "./pages/Admin/conference/CreateConference";
import UpdateConference from "./pages/Admin/conference/UpdateConference";
import DeleteConference from "./pages/Admin/conference/DeleteConference";
import ListConference from "./pages/Admin/conference/ListConference";

/* ===== RBAC ===== */
import RbacManagement from "./pages/Admin/rbac/RbacManagement";

/* ===== SYSTEM ===== */
import SystemOverview from "./pages/Admin/system/SystemOverview";
import SmtpConfig from "./pages/Admin/system/SmtpConfig";
import EmailQuota from "./pages/Admin/system/EmailQta";
import AuditLogs from "./pages/Admin/system/AuditLogs";
import Backup from "./pages/Admin/system/Backup";
import Restore from "./pages/Admin/system/Restore";

/* ===== AI ===== */
import AiOverview from "./pages/Admin/AI/AiOverview";
import AiToggle from "./pages/Admin/AI/AiToggle";
import AiLogs from "./pages/Admin/AI/AiLogs";

/* ===== CHAIR ===== */
import ChairWorkflow from "./pages/Chair/ChairWorkflow";

/* ===== REVIEWER ===== */
import ReviewerPaperList from "./pages/Reviewer/ReviewerPaperList";
import PaperDetail from "./pages/Reviewer/PaperDetail";

import MainLayoutReviewer from "./layouts/MainLayoutReviewer";
import DashboardReviewer from "./pages/Reviewer/DashboardReviewer";
import AssignedPapersReviewer from "./pages/Reviewer/AssignedPapersReviewer";
import ReviewActionReviewer from "./pages/Reviewer/ReviewActionReviewer";
import PaperDetailReviewer from "./pages/Reviewer/PaperDetailReviewer";
import SubmitReview from "./pages/Reviewer/SubmitReview";
import DeclineReview from "./pages/Reviewer/DeclineReview";
import DeclareCOIDetailsReviewer from "./pages/Reviewer/DeclareCOIDetailsReviewer";

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
        <Route path="/conference-manage/edit" element={<EditUser />} />

        {/* CHAIR */}
        <Route path="/chair" element={<ChairWorkflow />} />

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
