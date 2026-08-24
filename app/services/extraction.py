from app.schemas import MeetingExtraction


def extract_meeting(raw_text: str) -> MeetingExtraction:
    """STT 원문 텍스트 → 구조화 추출.

    TODO: my_service_structured.py의 RCIF_V4 프롬프트 + LangChain 체인을 이식.
    사용자 입력(raw_text)은 프롬프트에서 지시가 아니라 데이터로 취급할 것
    (PRD-MVP.md 6절 프롬프트 인젝션 완화 조치).
    """
    raise NotImplementedError
