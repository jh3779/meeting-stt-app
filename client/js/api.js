// 백엔드(FastAPI) 호출 전용 — 앱은 Firestore를 직접 알지 못함 (PRD-MVP.md 4절)
// 로컬에서 8000번 포트가 다른 프로젝트와 겹치는 등의 이유로 백엔드 주소를
// 바꿔야 하면 ?api=http://localhost:8001 쿼리 파라미터로 덮어쓸 수 있음
// (한 번 지정하면 페이지 이동 중에도 sessionStorage로 유지됨).
const apiParam = new URLSearchParams(window.location.search).get("api");
if (apiParam) sessionStorage.setItem("apiBaseUrl", apiParam);
const API_BASE_URL =
  apiParam || sessionStorage.getItem("apiBaseUrl") || window.API_BASE_URL || "http://localhost:8000";

function friendlyErrorMessage(status, detail) {
  if (status === 404) return "회의를 찾을 수 없습니다.";
  if (status === 413) return detail || "입력한 텍스트가 너무 깁니다.";
  if (status >= 500) return "서버에 오류가 발생했습니다. 잠시 후 다시 시도해주세요.";
  return detail || "요청을 처리하지 못했습니다.";
}

async function apiRequest(path, options) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const rawBody = await response.text();
    let detail;
    try {
      detail = JSON.parse(rawBody).detail;
    } catch {
      detail = undefined;
    }
    console.error(`API error ${response.status} on ${path}:`, rawBody);
    throw new Error(friendlyErrorMessage(response.status, detail));
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
