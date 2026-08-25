// index.js와 detail.js가 함께 쓰는 회의 렌더링 로직 — 같은 데이터가
// 페이지마다 다르게 보이지 않도록 여기 한 곳에서만 만든다.

function createStatusBadge(status) {
  const badge = document.createElement("span");
  badge.className = "badge";
  badge.dataset.status = status;
  badge.textContent = status;
  return badge;
}

function renderDecisions(container, decisions) {
  container.innerHTML = "";
  if (decisions.length === 0) {
    const empty = document.createElement("li");
    empty.className = "empty-state";
    empty.textContent = "결정사항이 없습니다.";
    container.appendChild(empty);
    return;
  }
  for (const decision of decisions) {
    const li = document.createElement("li");
    li.textContent = decision;
    container.appendChild(li);
  }
}

function renderActionItems(container, items) {
  container.innerHTML = "";
  if (items.length === 0) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.className = "empty-state";
    td.colSpan = 3;
    td.textContent = "액션아이템이 없습니다.";
    tr.appendChild(td);
    container.appendChild(tr);
    return;
  }
  for (const item of items) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td></td><td></td><td></td>`;
    tr.children[0].textContent = item.task;
    tr.children[1].textContent = item.owner;
    tr.children[2].textContent = item.deadline ?? "-";
    container.appendChild(tr);
  }
}
