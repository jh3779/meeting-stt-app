# meeting-stt-app

LG CNS AI Campus 과정 "DB 파트" 미니 프로젝트 — 옆사람과 2인으로 진행. STT로 변환된 회의록 텍스트를 구조화해 추출하고(지난주 LLM 실습 재사용), Firestore에 저장·조회하는 서비스.

## 기획 문서

- [`docs/PRD-MVP.md`](docs/PRD-MVP.md) — 실제로 만들 범위(MVP), 아키텍처, 스코프 가드레일, 최소 보안 조치
- [`docs/PRD-MAIN.md`](docs/PRD-MAIN.md) — MVP 이후 확장 계획(Whisper API 연동·인증·Redis 등)
- [`docs/ERD.md`](docs/ERD.md) — Firestore 데이터 모델(`meetings` 컬렉션) + RDBMS로 설계했다면의 비교

아직 구현 전 — 문서 우선, 코드는 빈 스캐폴드만 있는 단계입니다.

## 디렉터리 구조

```text
app/       백엔드(FastAPI, PRD-MVP 8절 API 개요 기준)
client/    앱(클라이언트) — 아키텍처상 Firestore에 직접 접근하지 않고 항상 app/을 거침
docs/      기획 문서(PRD-MVP·PRD-MAIN·ERD)
```

## 아키텍처 한 줄 요약

```
앱(client) → FastAPI(app) → LLM 체인(구조화 추출) → Firestore(meetings 컬렉션)
```

앱은 Firestore 서비스 계정 키를 알지 못합니다 — 항상 백엔드를 거칩니다(PRD-MVP.md 4절, 보안 결정).

## 환경 변수

`.env.example` 참고 — Firestore 서비스 계정 키(`serviceAccountKey.json`)와 OpenAI API 키가 필요합니다. 실제 값은 `.env`/`serviceAccountKey.json`에 채우고 절대 커밋하지 마세요.
