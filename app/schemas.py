from datetime import datetime

from pydantic import BaseModel, Field


class ActionItem(BaseModel):
    task: str
    owner: str = "명시 안 됨"
    deadline: str | None = None


class MeetingExtraction(BaseModel):
    """LLM 구조화 추출 결과. ERD.md 1절의 Firestore 문서 스키마와 1:1 매핑."""

    title: str = "제목 없음"
    meeting_date: str
    status: str
    decisions: list[str] = Field(default_factory=list)
    action_items: list[ActionItem] = Field(default_factory=list)


class MeetingExtractRequest(BaseModel):
    raw_text: str


class MeetingExtractResponse(MeetingExtraction):
    id: str


class MeetingSummary(BaseModel):
    id: str
    title: str
    meeting_date: str
    status: str
    created_at: datetime | None = None


class MeetingDetail(MeetingSummary):
    raw_text: str
    decisions: list[str]
    action_items: list[ActionItem]
