# 작업 로그 및 설계 근거 검토

> 상태: 2026-08-24~25 세션 기록. 이 문서는 코드가 바뀔 때마다 갱신하는 살아있는 문서가 아니라 **이 세션에서 한 일을 나중에 되짚어보기 위한 스냅샷**이다. 최신 코드 상태는 코드 자체와 [DESIGN.md](../DESIGN.md)·[CONTRIBUTING.md](../CONTRIBUTING.md)를 우선한다.
>
> 작성 기준: `db-firestore` 브랜치, 마지막 push는 `7175d60`. 8/26(수) 오전 평가 + 오후 발표 기준으로 남은 시간이 많지 않다는 점을 감안해, 항목마다 **근거**와 함께 **검토(잘 됐는지, 리스크는 뭔지)**를 같이 적었다.

## 0. 요약

| 영역 | 상태 |
|---|---|
| 백엔드 스캐폴드 + CI + pre-commit | `master`에 커밋·push 완료 |
| 브랜치 규칙 문서화 | 문서로만 존재, GitHub 저장소 설정(Branch protection)에는 미적용 |
| 프롬프트 체인(PR #1) | 병합 완료, 단 **실제 OpenAI 호출로 검증된 적 없음** (아래 5-3 참고) |
| DB(Firestore) 연동 | `db-firestore` 브랜치에 커밋됨, 로컬 에뮬레이터로만 검증 |
| 프론트엔드 디자인 폴리시 | **아직 커밋 안 됨** — `db-firestore` 브랜치에 스테이징만 되어 있음 |
| 실제 브라우저 렌더링 확인 | **한 번도 못 함** — 이 세션엔 브라우저 자동화 도구가 없었음 |

## 1. 백엔드/인프라 뼈대

### 한 일
- `app/`에 FastAPI 스캐폴드(`main.py`, `routers/meetings.py`, `schemas.py`, `config.py`, `services/`) 구성. PRD-MVP.md 8절의 API 개요(`POST /meetings/extract`, `GET /meetings`, `GET /meetings/{id}`)를 그대로 반영.
- `.pre-commit-config.yaml`: 공통 위생 훅(trailing-whitespace, EOF, yaml/large-file/merge-conflict 체크) + 백엔드 `ruff` lint/format.
- `.github/workflows/ci.yml`: 백엔드(lint+test) / 클라이언트(JS 문법 체크) 두 잡.
- `CONTRIBUTING.md`: master 직접 push 금지, PR+CI+리뷰 1건 필수, squash merge 규칙.

### 근거
- API 형태는 PRD에 이미 명시돼 있어 새로 설계할 필요가 없었음 — 문서를 코드로 그대로 옮김.
- pre-commit에 클라이언트용 prettier 훅을 넣으려 했으나 이 머신의 npm이 git 설치를 막고 있어(`EALLOWGIT`) 실패 → 제거. 클라이언트는 순수 정적 파일이라 대신 CI에서 `node --check`로 최소한의 문법 검증만 하도록 스코프를 낮춤.

### 검토
- CI가 실제로 동작하는지는 이후 PR #1에서 실전 검증됨(아래 3-3) — 의도대로 lint 실패를 잡아냈다.
- **브랜치 보호 규칙은 문서로만 존재한다.** GitHub 저장소 설정(Settings → Branches)에 실제 Branch protection rule을 걸지 않기로 사용자가 명시적으로 선택했음(2026-08-24) — 즉 지금도 누구나 `master`에 직접 push할 수 있다. 실제로 이 세션에서도 사용자 지시로 여러 번 `master`에 직접 push했다(PRD 문서 수정 등). 문서상 규칙과 실제 강제력이 불일치하는 상태이므로, 발표 전까지 사고 없이 넘어가는 건 "다들 조심해서"에 의존하고 있다는 점은 인지하고 있어야 한다.

## 2. 협업 워크플로우

### 한 일
- `app/services/extraction.py`(프롬프트 담당)와 `app/services/firestore_client.py`(DB 담당)에 각각 담당자용 가이드라인 주석 추가 — 입력/출력 계약, 보안 요구사항(프롬프트 인젝션 방어), 확장 시 참고 지점을 코드 안에 명시.
- `db-firestore`(본인 작업용), `prompt-chain`(옆사람 작업 시작점) 두 브랜치를 `master`에서 분기해 생성.

### 근거
- 옆사람이 "프롬프트를 전담"하기로 한 역할 분담(2026-08-24 대화)을 코드 수준에서 명확히 하기 위함 — PRD-MVP.md 10절의 "역할 분담 — 옆사람과 논의 필요"라는 열린 질문을 실질적으로 좁혀준 것.

### 검토
- **`prompt-chain` 브랜치는 결국 안 쓰였다.** 옆사람은 실제로 `jeongmunseob`라는 별도 브랜치를 만들어 PR #1을 올렸다 — `prompt-chain`은 `master`(`f13cd9d`) 시점에 멈춰 있는 죽은 브랜치로 남아 있다. 브랜치 이름을 미리 정해준 것 자체는 무의미하지 않았지만(가이드라인 주석이 방향을 잡아준 건 사실), 실제 협업은 GitHub에서 각자 편한 브랜치명으로 이뤄졌다 → **정리 필요**: `prompt-chain`(로컬+원격)과 로컬에 남은 `jeongmunseob` 브랜치(원격은 병합 후 자동 삭제됨)를 지울지 사용자 판단이 필요하다.

## 3. PR #1 병합 — 가장 판단이 많이 들어간 작업

### 한 일
- 옆사람이 올린 PR #1(`jeongmunseob` → `master`, "Update extraction.py")의 CI가 실패 중이었음. 원인 진단 후:
  - `app/services/my_service_structured.py`를 새로 작성 — 실제 LangChain 체인(`ChatOpenAI` + `with_structured_output(MeetingExtraction)`), 프롬프트 인젝션 방어용 시스템 프롬프트 포함.
  - `app/services/extraction.py`를 라우터가 참조하는 안정적 진입점으로 복원(위 모듈을 재노출).
  - 옆사람이 `extraction.py` 안에 잘못 넣어둔 pytest 테스트 3개를 `app/tests/test_my_service_structured.py`로 이동(원래 위치는 `pytest.ini`의 `testpaths=app/tests` 밖이라 CI가 아예 수집하지 못하고 있었음).
  - `app/config.py`에 `openai_model` 설정 추가(테스트가 기대하던 필드).
  - 수정을 `jeongmunseob` 브랜치에 커밋·push → CI 재실행 → 통과 확인 → squash merge.

### 근거
- CI 실패의 진짜 원인은 두 가지였다: ①테스트가 참조하는 `my_service_structured.py` 구현 파일 자체가 PR에 없었음, ②`extract_meeting()` 함수가 통째로 삭제되어 라우터 임포트가 깨짐. 둘 다 "리뷰 코멘트 남기고 기다리기"로는 마감(8/26) 안에 해결이 안 될 가능성이 높아 사용자 승인(2회: "진행해봐")을 받고 직접 구현했다.
- 테스트 위치 이동은 옆사람이 작성한 테스트 코드(모킹 대상, assertion)는 그대로 두고 파일 위치와 import 정렬만 고친 것 — 로직을 임의로 바꾸지 않음.

### 검토 (여기가 가장 신경 써서 봐야 할 부분)
- **가장 큰 리스크: 실제 프롬프트 내용을 내가 썼다.** `my_service_structured.py`의 시스템 프롬프트(회의 판별 기준, 필드별 규칙)는 옆사람이 작성한 적 없는, 내가 새로 쓴 내용이다. "프롬프트는 옆사람 담당"이라는 역할 분담과 어긋난다 — CI를 통과시키기 위한 최소 구현이었지만, **옆사람이 이 프롬프트 문구를 직접 검토하고 필요하면 고쳐야 한다.** 특히:
  - 회의/비회의 판별 기준("실제 회의 내용이면 회의록, 잡담이면 회의록아님")이 옆사항이 1주차에 실제로 쓰던 판별 로직과 같은지 확인 안 됨.
  - `gpt-4o-mini`를 기본 모델로 넣었는데, 이게 원래 쓰던 모델인지도 확인 안 됨(`app/config.py`의 `openai_model` 기본값).
- **한 번도 실제 OpenAI API를 호출해서 검증하지 않았다.** 테스트 3개는 전부 `ChatOpenAI`를 mock으로 대체한 유닛 테스트다. 즉 "코드가 문법적으로 맞고 mock 기준으로는 동작한다"까지만 확인됐고, **실제 LLM이 이 프롬프트로 기대한 형태의 JSON을 안정적으로 반환하는지는 이 세션에서 단 한 번도 실행해보지 않았다.** 발표 전 최소 1회는 실제 회의록 텍스트로 end-to-end 테스트가 필요하다(토큰이 걱정되면 아주 짧은 샘플 1~2개만이라도).
- squash merge는 CONTRIBUTING.md가 규정한 방식과 일치하지만, PR에 팀원 리뷰 승인(reviewDecision)이 없는 상태로 병합했다 — CONTRIBUTING.md 3번 규칙("팀원 리뷰 승인 1건 이상 후 병합")을 형식적으로는 어겼다. 사용자 승인 하에 진행했지만, 실제 옆사람이 리뷰할 기회는 없었다는 점은 남는다.

## 4. 로컬 개발 환경

### 한 일
- `.venv` 생성, `pre-commit install`.
- `docker-compose.yml`(옆사람이 이미 추가해둔 것)로 로컬 Firestore 에뮬레이터 기동, `FIRESTORE_EMULATOR_HOST`로 실제 서비스 계정 키 없이 DB 계층 테스트.
- **CORS 버그 발견/수정**: `app/main.py`에 `CORSMiddleware`가 없어서, 정적 클라이언트(`client/`)가 브라우저에서 API를 호출하면 무조건 막히는 상태였음 — `allow_origins=["*"]`로 추가.
- `client/js/api.js`에 `?api=` 쿼리 파라미터로 백엔드 주소를 바꿀 수 있게 하고 `sessionStorage`로 페이지 이동 간 유지되게 함(로컬 8000번 포트가 다른 프로젝트와 충돌해서 8001을 써야 했던 상황 대응).
- Firestore 에뮬레이터에 LLM 호출 없이 샘플 회의 문서 3건을 직접 저장(토큰 절약 목적) + 수동 테스트용 임시 STT 스크립트 2개(scratchpad, repo에는 없음).

### 근거
- CORS는 실제로 브라우저에서 클라이언트를 열어봤다면 바로 걸렸을 문제인데, 브라우저 자동화가 없어서 curl로 `access-control-allow-origin` 헤더 유무를 직접 확인해서 찾아냄.
- 토큰 절약: `CONTRIBUTING.md`에 옆사람이 이미 남겨둔 "OpenAI 토큰 아끼는 법" 원칙(에뮬레이터+픽스처로 DB 계층만 검증)을 그대로 따름.

### 검토
- `allow_origins=["*"]`는 인증이 아예 없는 MVP 단계에서는 괜찮지만, PRD-MAIN.md의 Firebase Auth 도입 시점엔 반드시 특정 origin으로 좁혀야 한다 — 지금 상태로 Main 단계까지 그대로 가면 안 됨(현재 DESIGN.md/코드 어디에도 이 경고가 명시적으로 안 남아 있어서, 이 문서에라도 남겨둔다).
- 에뮬레이터 시드 데이터는 **휘발성**이다(`docker compose down`하면 사라짐, 볼륨 마운트 안 함). 발표 데모에 쓸 실제 데이터가 아니라 순수 개발 확인용.
- 정적 서버(포트 5500)와 백엔드(포트 8001)는 이 세션에서 수동으로 띄운 백그라운드 프로세스라 터미널/머신을 재시작하면 사라진다 — 실행 방법은 [README.md](../README.md)의 "시작하기" 절 참고.

## 5. 프론트엔드 디자인

### 한 일 (1차: 가벼운 폴리시)
- 디자인 토큰 도입(색/spacing/radius/shadow), 다크모드(`prefers-color-scheme`), 카드형 패널, 상태 배지, 목록/상세 페이지 레이아웃 정리.

### 한 일 (2차: `design-review` 스킬 — critique + audit + document)
- **critique**: 두 개의 독립 서브에이전트(디자인 리뷰 / 탐지 증거)를 병렬 실행해 종합. 탐지 스크립트(`detect.mjs`)가 이 환경에 없어서, 탐지 역할은 실제 hex 값으로 WCAG 대비비를 계산하는 수동 스캔으로 대체.
- **주요 수정**:
  - 추출 결과가 raw JSON으로 표시되던 것을 상세 페이지와 동일한 구조화 UI로 통일(`client/js/render.js` 공유 렌더러 도입) — 이를 위해 백엔드 `POST /meetings/extract` 응답에 `id` 필드 추가(`MeetingExtractResponse`).
  - WCAG AA 대비 실패(`--color-text-tertiary`가 본문 텍스트로 쓰이던 것) 수정 — `--color-text-secondary`로 교체.
  - `detail.js`에서만 에러 시 빨간 스타일이 안 먹던 버그 수정, 백엔드 원문 에러가 그대로 노출되던 것을 한국어 메시지로 매핑.
  - 뒤로가기 링크 터치 타깃 확대, 액션아이템 표에 가로 스크롤 래퍼 추가.
  - **작업 도중 자체적으로 만든 버그 2건도 그 자리에서 발견해 수정**: 배지를 `replaceWith`로 교체하면서 id가 사라져 재추출 시 깨지던 문제, 결정사항 리스트 스타일이 ID 선택자에 묶여 있어 새로 만든 결과 화면엔 적용이 안 되던 문제.
- **document**: `DESIGN.md` 신규 작성(토큰 frontmatter + 8개 표준 섹션).

### 근거
- "웹 디자인 스킬 사용해줘" → "일단 전체 적용해줘"라는 명시적 사용자 지시에 따라 critique/audit/document 세 커맨드를 모두 실행. 세 커맨드 다 "Evaluate/Build" 카테고리라 원래는 발견 사항만 보고하고 사용자에게 우선순위를 물어야 하지만(critique.md의 "Ask the User" 단계), "전체 적용해줘"를 스코프에 대한 답으로 해석해 발견된 P1/P2를 바로 고치는 쪽으로 진행했다.

### 검토
- **가장 큰 한계: 실제 브라우저에서 눈으로 확인한 적이 없다.** 이 세션 내내 브라우저 자동화 도구가 연결되어 있지 않았다. 대비비 계산, JS 문법 체크, CSS 중괄호 짝 확인 등 "기계적으로 검증 가능한 것"은 다 했지만, 실제 레이아웃이 의도한 대로 보이는지는 **한 번도 스크린샷으로 확인하지 못했다.** 발표 전 반드시 브라우저로 직접 열어봐야 한다(`client/list.html?api=http://localhost:8001` 등 — 이전 대화에 URL 남겨둠).
- Assessment B(탐지 서브에이전트)가 "다크모드에서 `--color-danger-soft-bg` 누락"이라고 보고했는데, 실제 파일을 다시 읽어보니 **오탐이었다**(양쪽 다 이미 정의돼 있었음). 서브에이전트 보고를 그대로 믿지 않고 검증한 사례 — 반대로 말하면 다른 보고 중에도 이런 오탐이 더 있을 수 있으니, 이 문서의 "수정한 것" 목록도 100% 무결하다고 과신하지 않는 게 좋다.
- 수정/삭제 기능 부재(P1)는 발견됐지만 **의도적으로 고치지 않았다** — API 자체에 없는 기능이라 디자인 스킬 범위를 넘어서는 제품 결정이라 판단했음. 발표에서 "왜 회의록을 잘못 저장하면 못 고치나요?"라는 질문이 나올 수 있다는 점은 미리 인지하고 있는 게 좋다.
- **이 모든 프론트엔드 변경은 아직 커밋되지 않았다.** `git status`에 스테이징 상태로만 남아 있다(`app/main.py`, `app/routers/meetings.py`, `app/schemas.py`, `client/*`, `DESIGN.md`). 커밋·push를 원하면 별도로 요청해야 한다.

## 6. 마감(8/26) 전 남은 것 — 체크리스트

- [ ] **실제 OpenAI API로 `extract_meeting()` 최소 1회 end-to-end 테스트** (지금까지 전부 mock/에뮬레이터로만 검증됨)
- [ ] **브라우저로 직접 3페이지 열어서 눈으로 확인** (CORS 수정, 디자인 폴리시 전부 시각적으로 미검증)
- [ ] 옆사람에게 `my_service_structured.py`의 프롬프트 내용 검토 요청(내가 대신 쓴 부분)
- [ ] 현재 스테이징된 프론트엔드/백엔드 변경사항 커밋·push 여부 결정
- [ ] 실제 serviceAccountKey.json으로 Firestore 연결 최소 1회 확인(지금까지는 에뮬레이터만 사용)
- [ ] `prompt-chain`(안 쓰인 브랜치), 로컬 `jeongmunseob` 브랜치 정리 여부 결정
- [ ] GitHub 브랜치 보호 규칙을 실제로 걸지, 문서로만 남길지 재확인
- [ ] 발표 자료 준비(담당자 미정 — PRD-MVP.md 10절 열린 질문)
