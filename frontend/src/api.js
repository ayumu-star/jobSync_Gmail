// src/api.js

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

async function apiFetch(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  let data = {};
  try {
    data = await res.json();
  } catch (e) {
    // JSONじゃないレスポンスは無視
  }

  if (!res.ok) {
    throw { status: res.status, data };
  }

  return data;
}

export const api = {
  loginWithGoogle(token) {
    return apiFetch("/api/auth/google", {
      method: "POST",
      body: JSON.stringify({ token }),
    });
  },

  logout() {
    return apiFetch("/api/auth/logout", { method: "POST" });
  },

  getCurrentUser() {
    return apiFetch("/api/user");
  },

  getGmailAuthorizeUrl() {
    return apiFetch("/api/gmail/authorize");
  },

  getEmails() {
    return apiFetch("/api/gmail");
  },

  // ★ ここから追加（or 修正）
  fetchEvents() {
    return apiFetch("/api/events");
  },

  syncEvents() {
    return apiFetch("/api/events/sync", {
      method: "POST",
    });
  },
};

