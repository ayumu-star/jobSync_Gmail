// frontend/src/pages/HomePage.jsx
import React from "react";
import { Link } from "react-router-dom";
import { mockEmails, mockEvents } from "../mockData";

export default function HomePage() {
  return (
    <div className="page">
      <div className="page-grid">
        {/* 左：未処理メール */}
        <section>
          <h2 className="section-title">未処理メール</h2>
          <p className="section-subtitle">
            企業から届いた案内メールのうち、まだ予定に登録していないものです。
          </p>
          <div className="list-stack">
            {mockEmails.map((email) => (
              <Link
                key={email.id}
                to={`/emails/${email.id}`}
                className="card card-link"
              >
                <div className="card-meta">
                  {email.receivedAt} ／ {email.from}
                </div>
                <div className="card-title">{email.subject}</div>
              </Link>
            ))}
          </div>
        </section>

        {/* 右：登録済みイベント */}
        <section>
          <h2 className="section-title">登録済みイベント</h2>
          <p className="section-subtitle">
            面接・説明会など、カレンダーに登録済みの予定の一覧です。
          </p>
          <div className="list-stack">
            {mockEvents.map((ev) => (
              <Link
                key={ev.id}
                to={`/events/${ev.id}`}
                className="card card-link"
              >
                <div className="card-meta">
                  {ev.date} {ev.time}
                </div>
                <div className="card-title">{ev.title}</div>
                <div className="card-sub">
                  {ev.company} ／ {ev.type}
                </div>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
