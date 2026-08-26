# 브랜치 & 협업 규칙

2인 미니 프로젝트 기준. 브랜치 이름 형식은 강제하지 않음 — 아래는 병합 절차만 규정.

## 규칙

1. **`master`에 직접 push 금지.** 모든 변경은 `master`에서 새 브랜치를 파서 작업하고, PR을 통해서만 `master`에 반영한다.
2. **PR 병합 전 CI 통과 필수** — `.github/workflows/ci.yml`의 backend(lint+test)·client(문법 체크) 잡이 모두 성공해야 한다.
3. **팀원 리뷰 승인 1건 이상 후 병합.** 2인 프로젝트이므로 상대방 승인 없이 셀프 머지하지 않는다.
4. **Squash merge로 병합**하고, 병합 후 브랜치는 삭제한다 — `master` 히스토리를 기능 단위로 깔끔하게 유지.
5. **`master`는 항상 동작하는 상태를 유지한다.** 실행이 깨지는 커밋을 `master`에 남기지 않는다(시연 직전 마스터가 깨지는 상황 방지).

## 로컬 개발 전 1회 설정

```bash
pip install -r app/requirements-dev.txt pre-commit
pre-commit install
```

커밋할 때마다 `.pre-commit-config.yaml`에 정의된 검사(공백/개행 정리, 백엔드 ruff lint·format)가 자동 실행된다.

## DB(Firestore) 로직만 테스트하기 — OpenAI 토큰 아끼는 법

`POST /meetings/extract`를 실제로 호출하면 매번 `extract_meeting()`이 OpenAI를 호출한다.
수업에서 받은 토큰은 한정돼 있으니, **DB 저장/조회 로직만 확인하고 싶을 때는 실제
LLM을 부르지 말고 아래 방식을 쓴다** — extraction.py가 아직 미구현이어도 이 방식으로
라우터·Firestore 연동은 먼저 검증할 수 있다.

1. 로컬 Firestore 에뮬레이터 실행(서비스 계정 키·클라우드 비용 필요 없음):
   ```bash
   docker compose up -d
   ```
2. `.env`에 `FIRESTORE_EMULATOR_HOST=localhost:8080` 추가(`.env.example` 참고).
3. DB 계층만 검증하는 테스트 실행 — `extract_meeting()`을 픽스처로 대체해서 실제로
   OpenAI를 부르지 않는다:
   ```bash
   FIRESTORE_EMULATOR_HOST=localhost:8080 pytest app/tests/test_meetings_with_emulator.py -v
   ```
   - 픽스처: `app/tests/fixtures/sample_meeting_transcript.txt`(가상 STT 원문) +
     `sample_meeting_extraction.json`(그에 대응하는 가짜 구조화 결과) — 둘 다 실제
     수업 녹취가 아닌 완전히 지어낸 시나리오라 자유롭게 커밋·공유해도 됨.
4. 다 쓰면 에뮬레이터 종료: `docker compose down`

실제 LLM 체인(`extract_meeting`)까지 붙여서 진짜로 확인해야 할 때만 `.env`에서
`FIRESTORE_EMULATOR_HOST`를 비우고(또는 주석 처리) 실제 Firestore+OpenAI로 테스트한다 —
이때는 최소 횟수로만 확인할 것.
