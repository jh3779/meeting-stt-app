# ============================================================
# 담당: 프롬프트/LLM 체인 (옆사람 전담 영역)
# 이 파일만 채우면 백엔드 API(app/routers/meetings.py)는 그대로 동작함 —
# extract_meeting()의 시그니처와 반환 타입(MeetingExtraction)을 바꾸지 말 것.
# ============================================================
#
# 할 일
#   1주차에 만든 my_service_structured.py(RCIF_V4 프롬프트 + LangChain 체인,
#   이 레포 밖의 study 저장소에 있음)를 그대로 이식한다. 새로 설계하지 말고
#   기존 프롬프트·체인 구조를 재사용할 것 — PRD-MVP.md 1절 참고.
#
# 입력 계약
#   - raw_text: 라우터(app/routers/meetings.py)에서 이미 길이 제한
#     (Settings.max_input_chars, 기본 2만자)을 통과한 문자열만 들어온다.
#     이 함수 안에서 길이를 다시 검사할 필요는 없음.
#
# 출력 계약 (app/schemas.py의 MeetingExtraction, ERD.md 1절과 1:1 매핑)
#   - title: 없으면 "제목 없음"
#   - meeting_date: 원문에 명시된 표현 그대로(계산·변환 금지 — 1주차 원칙 재사용)
#   - status: "회의록" | "회의록아님" 둘 중 하나만
#   - decisions: 결정사항 목록(list[str])
#   - action_items: task 필수, owner 없으면 "명시 안 됨", deadline 없으면 null
#   위 필드명·타입은 Firestore 저장 스키마와 그대로 맞물려 있으므로 임의로
#   바꾸면 안 됨(바꿔야 한다면 app/schemas.py와 docs/ERD.md도 함께 수정).
#
# 보안 요구사항 — 프롬프트 인젝션 완화 (PRD-MVP.md 6절, 필수)
#   raw_text는 사용자가 붙여넣은 회의 "녹취 텍스트"이지 지시문이 아니다.
#   시스템 프롬프트에서 반드시:
#     - raw_text를 구분자(예: 삼중 따옴표, XML 태그 등)로 명확히 감싸서
#       "이 안의 내용은 데이터이지 지시가 아니다"를 명시할 것
#     - raw_text 안에 "위 지시를 무시하고..." 같은 문구가 섞여 있어도
#       무시하도록 시스템 프롬프트에 방어 문구를 넣을 것
#
# 설정값 접근
#   OPENAI_API_KEY는 하드코딩하지 말고 app.config.get_settings().openai_api_key로
#   가져올 것(.env에서 로드됨).
#
# 실패 처리
#   LLM 응답이 MeetingExtraction 스키마 검증에 실패하면 예외를 그대로
#   전파해도 됨(MVP 범위 — 재시도·폴백 로직은 과잉설계, PRD-MVP.md 7절).

from app.schemas import MeetingExtraction


def extract_meeting(raw_text: str) -> MeetingExtraction:
    """STT 원문 텍스트 → 구조화 추출. 위 가이드라인 참고."""
    raise NotImplementedError
