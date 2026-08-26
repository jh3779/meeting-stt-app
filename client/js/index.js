const textArea = document.getElementById("raw-text");
const extractBtn = document.getElementById("extract-btn");
const statusEl = document.getElementById("status");
const resultSection = document.getElementById("result");
const charCountEl = document.getElementById("char-count");

const MAX_CHARS = Number(textArea.maxLength);

function updateCharCount() {
  charCountEl.textContent = `${textArea.value.length.toLocaleString("ko-KR")} / ${MAX_CHARS.toLocaleString("ko-KR")}자`;
}

textArea.addEventListener("input", updateCharCount);
updateCharCount();

extractBtn.addEventListener("click", async () => {
  const rawText = textArea.value.trim();
  delete statusEl.dataset.tone;
  if (!rawText) {
    statusEl.dataset.tone = "error";
    statusEl.textContent = "텍스트를 입력하세요.";
    return;
  }

  extractBtn.disabled = true;
  statusEl.textContent = "추출 중...";
  resultSection.hidden = true;

  try {
    const meeting = await api.extractMeeting(rawText);
    statusEl.textContent = "저장 완료.";

    document.getElementById("result-title").textContent = meeting.title;
    document.getElementById("result-date").textContent = meeting.meeting_date || "일시 미상";
    const statusBadgeContainer = document.getElementById("result-status-badge");
    statusBadgeContainer.innerHTML = "";
    statusBadgeContainer.appendChild(createStatusBadge(meeting.status));
    renderDecisions(document.getElementById("result-decisions"), meeting.decisions);
    renderActionItems(document.getElementById("result-action-items"), meeting.action_items);
    document.getElementById("result-link").href = `detail.html?id=${encodeURIComponent(meeting.id)}`;

    resultSection.hidden = false;
    textArea.value = "";
    updateCharCount();
  } catch (err) {
    statusEl.dataset.tone = "error";
    statusEl.textContent = `오류: ${err.message}`;
  } finally {
    extractBtn.disabled = false;
  }
});
