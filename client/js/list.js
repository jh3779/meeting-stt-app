const statusEl = document.getElementById("status");
const listEl = document.getElementById("meeting-list");

(async () => {
  statusEl.textContent = "불러오는 중...";
  try {
    const meetings = await api.listMeetings();
    statusEl.textContent = "";

    if (meetings.length === 0) {
      const empty = document.createElement("li");
      empty.className = "empty-state";
      empty.textContent = "저장된 회의가 없습니다.";

      const cta = document.createElement("a");
      cta.className = "empty-state-action";
      cta.href = "index.html";
      cta.textContent = "새 회의록 추가하기";
      empty.appendChild(document.createElement("br"));
      empty.appendChild(cta);

      listEl.appendChild(empty);
      return;
    }

    for (const meeting of meetings) {
      const li = document.createElement("li");
      const link = document.createElement("a");
      link.className = "meeting-row";
      link.href = `detail.html?id=${encodeURIComponent(meeting.id)}`;

      const info = document.createElement("span");
      info.className = "meeting-row-info";
      const title = document.createElement("span");
      title.className = "meeting-row-title";
      title.textContent = meeting.title;
      const date = document.createElement("span");
      date.className = "meeting-row-date";
      date.textContent = meeting.meeting_date || "일시 미상";
      info.appendChild(title);
      info.appendChild(date);

      link.appendChild(info);
      link.appendChild(createStatusBadge(meeting.status));
      li.appendChild(link);
      listEl.appendChild(li);
    }
  } catch (err) {
    statusEl.dataset.tone = "error";
    statusEl.textContent = `오류: ${err.message}`;
  }
})();
