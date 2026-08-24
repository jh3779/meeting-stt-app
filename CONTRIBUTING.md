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
