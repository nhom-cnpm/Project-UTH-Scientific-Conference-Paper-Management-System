import React from "react";
import { Outlet, Link } from "react-router-dom";

const MainLayout = () => {
  return (
    <div className="flex min-h-screen font-sans">
      {/* Sidebar */}
      <div className="w-64 bg-slate-50 border-r flex flex-col">
        <div className="p-6 text-xl font-bold text-gray-400">Review PC</div>
        <nav className="flex-1 px-4 space-y-2">
          <Link to="/" className="block p-3 hover:bg-blue-100 rounded">
            Home
          </Link>
          <Link
            to="/dashboard"
            className="block p-3 bg-blue-100 text-blue-700 rounded font-medium"
          >
            Dashboard
          </Link>
          <Link to="/assigned" className="block p-3 hover:bg-blue-100 rounded">
            Assigned Papers
          </Link>
          <button className="w-full text-left p-3 hover:bg-blue-100 rounded mt-10">
            Logout
          </button>
        </nav>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-[#43B5AD] text-white p-4 flex justify-between items-center">
          <h1 className="text-lg font-bold">UTH - COMFMS</h1>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-teal-700 rounded-full flex items-center justify-center">
              👤
            </div>
            <span>Reviewer ▼</span>
          </div>
        </header>

        {/* Page Content */}
        <main className="p-8 bg-white flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default MainLayout;
