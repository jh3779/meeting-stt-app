# meeting-stt-app

LG CNS AI Campus 과정 "DB 파트" 미니 프로젝트 — 옆사람과 2인으로 진행. STT로 변환된 회의록 텍스트를 구조화해 추출하고(지난주 LLM 실습 재사용), Firestore에 저장·조회하는 서비스.

## 기획 문서

- [`docs/PRD-MVP.md`](docs/PRD-MVP.md) — 실제로 만들 범위(MVP), 아키텍처, 스코프 가드레일, 최소 보안 조치
- [`docs/PRD-MAIN.md`](docs/PRD-MAIN.md) — MVP 이후 확장 계획(Whisper API 연동·인증·Redis 등)
- [`docs/ERD.md`](docs/ERD.md) — Firestore 데이터 모델(`meetings` 컬렉션) + RDBMS로 설계했다면의 비교

기본 뼈대(백엔드 FastAPI + 클라이언트 정적 HTML/JS)만 있는 단계 — 실제 추출 체인(`app/services/extraction.py`)은 아직 미구현(`NotImplementedError`)입니다.

## 디렉터리 구조

```text
app/       백엔드(FastAPI, PRD-MVP 8절 API 개요 기준)
client/    앱(클라이언트, 정적 HTML/CSS/JS) — 빌드 단계 없이 브라우저에서 바로 열어서 확인
docs/      기획 문서(PRD-MVP·PRD-MAIN·ERD)
```

## 시작하기

### 백엔드

```bash
pip install -r app/requirements-dev.txt
cp .env.example .env   # OPENAI_API_KEY 채우기, serviceAccountKey.json도 app/ 안에 배치
uvicorn app.main:app --reload
```

### 클라이언트

빌드 없이 정적 파일이므로 `client/index.html`을 브라우저로 바로 열거나, 정적 서버로 서빙하면 된다. 백엔드 주소가 `http://localhost:8000`이 아니면 페이지에서 `window.API_BASE_URL`을 설정한다.

### 협업 규칙

브랜치·PR·리뷰 절차는 [`CONTRIBUTING.md`](CONTRIBUTING.md) 참고.

## 아키텍처 한 줄 요약

```
앱(client) → FastAPI(app) → LLM 체인(구조화 추출) → Firestore(meetings 컬렉션)
```

앱은 Firestore 서비스 계정 키를 알지 못합니다 — 항상 백엔드를 거칩니다(PRD-MVP.md 4절, 보안 결정).

## 환경 변수

`.env.example` 참고 — Firestore 서비스 계정 키(`serviceAccountKey.json`)와 OpenAI API 키가 필요합니다. 실제 값은 `.env`/`serviceAccountKey.json`에 채우고 절대 커밋하지 마세요.
