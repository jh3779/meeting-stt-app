// 백엔드(FastAPI) 호출 전용 — 앱은 Firestore를 직접 알지 못함 (PRD-MVP.md 4절)
const API_BASE_URL = window.API_BASE_URL || "http://localhost:8000";

async function apiRequest(path, options) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`${response.status} ${response.statusText}: ${body}`);
  }
  return response.json();
}

const api = {
  extractMeeting: (rawText) =>
    apiRequest("/meetings/extract", {
      method: "POST",
      body: JSON.stringify({ raw_text: rawText }),
    }),
  listMeetings: () => apiRequest("/meetings"),
  getMeeting: (id) => apiRequest(`/meetings/${encodeURIComponent(id)}`),
};
