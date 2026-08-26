const statusEl = document.getElementById("status");
const detailEl = document.getElementById("meeting-detail");

(async () => {
  const id = new URLSearchParams(window.location.search).get("id");
  if (!id) {
    statusEl.textContent = "잘못된 접근입니다. 회의 id가 없습니다.";
    return;
  }

  statusEl.textContent = "불러오는 중...";
  try {
    const meeting = await api.getMeeting(id);
    statusEl.textContent = "";

    document.getElementById("meeting-title").textContent = meeting.title;
    document.getElementById("meeting-date").textContent = meeting.meeting_date || "일시 미상";

    const statusBadgeContainer = document.getElementById("meeting-status-badge");
    statusBadgeContainer.innerHTML = "";
    statusBadgeContainer.appendChild(createStatusBadge(meeting.status));

    renderDecisions(document.getElementById("meeting-decisions"), meeting.decisions);
    renderActionItems(document.getElementById("meeting-action-items"), meeting.action_items);

    detailEl.hidden = false;
  } catch (err) {
    statusEl.dataset.tone = "error";
    statusEl.textContent = `오류: ${err.message}`;
  }
})();
