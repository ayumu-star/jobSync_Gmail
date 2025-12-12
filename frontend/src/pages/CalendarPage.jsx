import { useEffect, useState } from "react";
import { api } from "../api";   // ★ ここを変更

export default function CalendarPage() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [error, setError] = useState(null);

  const loadEvents = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.fetchEvents();   // ★ 修正
      setEvents(data);
    } catch (e) {
      setError(e.message ?? "イベント取得に失敗しました");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, []);

  const handleSync = async () => {
    try {
      setSyncing(true);
      setError(null);
      const data = await api.syncEvents();   // ★ 修正
      setEvents(data);
    } catch (e) {
      setError(e.message ?? "同期に失敗しました");
    } finally {
      setSyncing(false);
    }
  };

  return (
    <div className="page calendar-page">
      <h1>就活カレンダー</h1>

      <button onClick={handleSync} disabled={syncing}>
        {syncing ? "同期中..." : "Gmailから同期"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {loading ? (
        <p>読み込み中...</p>
      ) : events.length === 0 ? (
        <p>まだ予定がありません。</p>
      ) : (
        <table className="events-table">
          <thead>
            <tr>
              <th>日付</th>
              <th>時間</th>
              <th>会社</th>
              <th>タイトル</th>
              <th>状態</th>
            </tr>
          </thead>
          <tbody>
            {events.map(ev => (
              <tr key={ev.id}>
                <td>{ev.start_at.slice(0, 10)}</td>
                <td>{ev.start_at.slice(11, 16)}</td>
                <td>{ev.company_name ?? "-"}</td>
                <td>{ev.title}</td>
                <td>{ev.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
