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
import ReviewerPaperList from "./pages/ReviewerPaperList";
import PaperDetail from "./pages/PaperDetail";

function App() {
  return (
    <Router>
      <Routes>
        {/* ===== PUBLIC ===== */}
        <Route path="/" element={<Trangchu />} />
        <Route path="/login" element={<Login />} />

        {/* ===== ADMIN CŨ ===== */}
        <Route path="/admin" element={<TrangcuaQtvien />} />
        <Route path="/adminPhanquyen" element={<TrangcuaQtvien />} />
        <Route path="/edituser/:id" element={<EditUser />} />

        {/* ===== ADMIN QUẢN LÝ HỘI NGHỊ ===== */}
       <Route path="/conference-manage" element={<AdminQuanli />}>
  <Route index element={<ListConference />} />

  {/* Conference */}
  <Route path="conference/create" element={<CreateConference />} />
  <Route path="conference/update/:id" element={<UpdateConference />} />
  <Route path="conference/delete/:id" element={<DeleteConference />} />

  {/* RBAC */}
  <Route path="rbac" element={<RbacManagement />} />

  {/* System */}
  <Route path="system">
    <Route index element={<SystemOverview />} />
    <Route path="smtp" element={<SmtpConfig />} />
    <Route path="email-quota" element={<EmailQuota />} />
    <Route path="audit-logs" element={<AuditLogs />} />
    <Route path="backup" element={<Backup />} />
    <Route path="restore" element={<Restore />} />
  </Route>

  {/* AI */}
  <Route path="ai">
    <Route index element={<AiOverview />} />
    <Route path="toggle" element={<AiToggle />} />
    <Route path="logs" element={<AiLogs />} />
  </Route>
</Route>


        {/* ===== CHAIR ===== */}
        <Route path="/chair" element={<ChairWorkflow />} />

        {/* ===== PROFILE ===== */}
        <Route path="/personalProfile" element={<PersonalProfile />} />

        {/* ===== REVIEWER ===== */}
        <Route path="/reviewer" element={<ReviewerLayout />}>
          <Route index element={<ReviewerPaperList />} />
          <Route path="paper/:id" element={<PaperDetail />} />
        </Route>

        {/* ===== FALLBACK ===== */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
