import { Routes, Route } from "react-router-dom";

import Login from "../pages/Login";
import Home from "../pages/Home";
import NotFound from "../pages/NotFound";

import DashboardLayout from "./layouts/DashboardLayout";
import ReviewerLayout from "../layouts/ReviewerLayout";
import ChairLayout from "../layouts/ChairLayout";

import ReviewerPaperList from "../pages/ReviewerPaperList";
import ChairPaperList from "../pages/ChairPaperList";
import PaperDetail from "../pages/PaperDetail";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />

      <Route
        path="/reviewer"
        element={
          <ReviewerLayout>
            <ReviewerPaperList />
          </ReviewerLayout>
        }
      />

      <Route
        path="/paper/:id"
        element={
          <ReviewerLayout>
            <PaperDetail />
          </ReviewerLayout>
        }
      />

      <Route
        path="/chair"
        element={
          <ChairLayout>
            <ChairPaperList />
          </ChairLayout>
        }
      />

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
