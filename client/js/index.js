const textArea = document.getElementById("raw-text");
const extractBtn = document.getElementById("extract-btn");
const statusEl = document.getElementById("status");
const resultSection = document.getElementById("result");
const resultJson = document.getElementById("result-json");

extractBtn.addEventListener("click", async () => {
  const rawText = textArea.value.trim();
  if (!rawText) {
    statusEl.textContent = "텍스트를 입력하세요.";
    return;
  }

  extractBtn.disabled = true;
  statusEl.textContent = "추출 중...";
  resultSection.hidden = true;

  try {
    const extraction = await api.extractMeeting(rawText);
    statusEl.textContent = "저장 완료.";
    resultJson.textContent = JSON.stringify(extraction, null, 2);
    resultSection.hidden = false;
  } catch (err) {
    statusEl.textContent = `오류: ${err.message}`;
  } finally {
    extractBtn.disabled = false;
  }
});
