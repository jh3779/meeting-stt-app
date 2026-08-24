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
    document.getElementById("meeting-date").textContent = meeting.meeting_date;
    document.getElementById("meeting-status").textContent = meeting.status;

    const decisionsEl = document.getElementById("meeting-decisions");
    for (const decision of meeting.decisions) {
      const li = document.createElement("li");
      li.textContent = decision;
      decisionsEl.appendChild(li);
    }

    const actionItemsEl = document.getElementById("meeting-action-items");
    for (const item of meeting.action_items) {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td></td><td></td><td></td>`;
      tr.children[0].textContent = item.task;
      tr.children[1].textContent = item.owner;
      tr.children[2].textContent = item.deadline ?? "-";
      actionItemsEl.appendChild(tr);
    }

    detailEl.hidden = false;
  } catch (err) {
    statusEl.textContent = `오류: ${err.message}`;
  }
})();
