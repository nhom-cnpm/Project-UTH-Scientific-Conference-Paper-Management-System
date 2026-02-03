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
import Home from "./pages/Home";
import ConferenceManage from "./pages/ConferenceManage";
import Dashboard from "./pages/Dashboard";


function App() {
  return (
    <Router>
      <Routes>
        {/* 1. Trang chủ hiện ngay lập tức tại đường dẫn gốc */}
        <Route path="/" element={<Home />} />

        {/* Đăng nhập */}
        <Route path="/login" element={<Login />} />

        {/* Dashboard - Chair */}
        <Route path="/chair" element={<ChairLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="conference" element={<ConferenceManage />} />
        </Route>

        {/* Dashboard - Reviewer */}
        <Route path="/reviewer" element={<ReviewerLayout />}>
          <Route index element={<ReviewerPaperList />} />
          <Route path="paper/:id" element={<PaperDetail />} />
        </Route>

        {/* Dashboard chung */}
        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<Dashboard />} />
        </Route>

        {/* Route không tồn tại */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
