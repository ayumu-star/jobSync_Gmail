// frontend/src/App.jsx
import React from "react";
import { Routes, Route, Link, useLocation } from "react-router-dom";

import HomePage from "./pages/HomePage";
import CalendarPage from "./pages/CalendarPage";
import EmailReviewPage from "./pages/EmailReviewPage";
import EventDetailPage from "./pages/EventDetailPage";

function Header() {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <header className="app-header">
      <div className="app-title">
        Tech Select
        <span>就活イベント整理アプリ</span>
      </div>
      <nav className="nav-links">
        <Link
          to="/"
          className={`nav-link ${isActive("/") ? "nav-link-active" : ""}`}
        >
          ホーム
        </Link>
        <Link
          to="/calendar"
          className={`nav-link ${
            isActive("/calendar") ? "nav-link-active" : ""
          }`}
        >
          カレンダー
        </Link>
      </nav>
    </header>
  );
}

export default function App() {
  return (
    <div className="app-root">
      <div className="app-shell">
        <Header />

        <main className="page">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/calendar" element={<CalendarPage />} />
            <Route path="/emails/:id" element={<EmailReviewPage />} />
            <Route path="/events/:id" element={<EventDetailPage />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}
