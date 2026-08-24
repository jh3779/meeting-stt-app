const statusEl = document.getElementById("status");
const listEl = document.getElementById("meeting-list");

(async () => {
  statusEl.textContent = "불러오는 중...";
  try {
    const meetings = await api.listMeetings();
    statusEl.textContent = "";
    if (meetings.length === 0) {
      statusEl.textContent = "저장된 회의가 없습니다.";
      return;
    }
    for (const meeting of meetings) {
      const li = document.createElement("li");
      const link = document.createElement("a");
      link.href = `detail.html?id=${encodeURIComponent(meeting.id)}`;
      link.textContent = `${meeting.meeting_date} — ${meeting.title}`;
      li.appendChild(link);
      listEl.appendChild(li);
    }
  } catch (err) {
    statusEl.textContent = `오류: ${err.message}`;
  }
})();
