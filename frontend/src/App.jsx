import React from "react";
import {
  BrowserRouter, // Chỉ dùng cái này
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

/* ===== ADMIN MỚI ===== */
import AdminQuanli from "./pages/Admin/AdminQuanli";

/* ===== CHAIR ===== */
import ChairWorkflow from "./pages/Chair/ChairWorkflow";

/* ===== REVIEWER ===== */
import ReviewerPaperList from "./pages/Reviewer/ReviewerPaperList";
import PaperDetail from "./pages/Reviewer/PaperDetail";
import DashboardReviewer from "./pages/Reviewer/DashboardReviewer";
import AssignedPapersReviewer from "./pages/Reviewer/AssignedPapersReviewer";
import ReviewActionReviewer from "./pages/Reviewer/ReviewActionReviewer";
import PaperDetailReviewer from "./pages/Reviewer/PaperDetailReviewer";
import SubmitReview from "./pages/Reviewer/SubmitReview";
import DeclineReview from "./pages/Reviewer/DeclineReview";
import DeclareCOIDetailsReviewer from "./pages/Reviewer/DeclareCOIDetailsReviewer";

/* ===== AUTHOR ===== */
import AuthorLayout from "./layouts/AuthorLayout";
import MySubmissionsAuthor from "./pages/Author/MySubmissionsAuthor";
import SubmissionDetailAuthor from "./pages/Author/SubmissionDetailAuthor";
import UploadCameraReady from "./pages/Author/UploadCameraReady";
import CreateSubmission from "./pages/Author/CreateSubmission";
import EditSubmission from "./pages/Author/EditSubmission";
import ViewReviewer from "./pages/Author/ViewReviewer";
import ViewDecision from "./pages/Author/ViewDecision";
import PersonalProfile from "./pages/Author/PersonalProfile";
import EditProfile from "./pages/Author/EditProfile";
import NotificationAuthor from "./pages/Author/NotificationAuthor";
import { SubmissionProvider } from "./pages/Author/SubmissionContext";

/* ===== Admin ===== */
import AiLogs from "./pages/Admin/AI/AiLogs";
import AiOverview from "./pages/Admin/AI/AiOverview";
import AiToggle from "./pages/Admin/AI/AiToggle";

import CreateConference from "./pages/Admin/conference/CreateConference";
import DeleteConference from "./pages/Admin/conference/DeleteConference";
import ListConference from "./pages/Admin/conference/ListConference";
import UpdateConference from "./pages/Admin/conference/UpdateConference";

import RbacManagement from "./pages/Admin/rbac/RbacManagement";

import AuditLogs from "./pages/Admin/system/AuditLogs";
import Backup from "./pages/Admin/system/Backup";
import EmailQta from "./pages/Admin/system/EmailQta";
import Restore from "./pages/Admin/system/Restore";
import SmtpConfig from "./pages/Admin/system/SmtpConfig";
import SystemOverview from "./pages/Admin/system/SystemOverview";


function App() {
  return (
    <SubmissionProvider>
      <BrowserRouter>
        <Routes>
          {/* ===== PUBLIC ===== */}
          <Route path="/" element={<Trangchu />} />
          <Route path="/login" element={<Login />} />

           {/* ===== ADMIN ===== */}
         <Route path="/admin" element={<AdminQuanli />}>
          
          {/* 1. Module Hội nghị (Mặc định hiển thị danh sách) */}
          <Route index element={<ListConference />} />
          <Route path="conference/create" element={<CreateConference />} />
          <Route path="conference/update/:id" element={<UpdateConference />} />
          <Route path="conference/delete/:id" element={<DeleteConference />} />

          {/* 2. Module RBAC */}
          <Route path="rbac" element={<RbacManagement />} />

          {/* 3. Module AI */}
          <Route path="ai" element={
            <>
              <AiToggle />
              <AiOverview />
              <AiLogs />
            </>
          } />

          {/* 4. Module System (Nested Routes bên trong System) */}
          <Route path="system">
            <Route index element={<SystemOverview />} />
            <Route path="smtp" element={<SmtpConfig />} />
            <Route path="email-quota" element={<EmailQta />} />
            <Route path="audit-logs" element={<AuditLogs />} />
            <Route path="backup" element={<Backup />} />
            <Route path="restore" element={<Restore />} />
          </Route>  
          </Route>Route


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

          {/* AUTHOR */}
          <Route path="/author" element={<AuthorLayout />}>
            <Route index element={<MySubmissionsAuthor />} />
            <Route
              path="submission-detail"
              element={<SubmissionDetailAuthor />}
            />
            <Route path="edit-submission" element={<EditSubmission />} />
            <Route path="view-reviewer/:id" element={<ViewReviewer />} />
            <Route path="view-decision/:id" element={<ViewDecision />} />
            <Route path="upload-camera-ready" element={<UploadCameraReady />} />
            <Route path="create-submission" element={<CreateSubmission />} />
            <Route path="personal-profile" element={<PersonalProfile />} />
            <Route path="edit-profile" element={<EditProfile />} />
            <Route path="notifications" element={<NotificationAuthor />} />
            <Route path="*" element={<Navigate to="/author" />} />
          </Route>

          {/* FALLBACK TOÀN HỆ THỐNG */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    </SubmissionProvider>
  );
}

export default App;
