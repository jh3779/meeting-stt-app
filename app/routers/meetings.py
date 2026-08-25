from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.schemas import (
    MeetingDetail,
    MeetingExtractRequest,
    MeetingExtractResponse,
    MeetingSummary,
)
from app.services.extraction import extract_meeting
from app.services.firestore_client import MEETINGS_COLLECTION, get_firestore_client

router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.post("/extract", response_model=MeetingExtractResponse)
def create_meeting(request: MeetingExtractRequest) -> MeetingExtractResponse:
    settings = get_settings()
    if len(request.raw_text) > settings.max_input_chars:
        raise HTTPException(
            status_code=413,
            detail=f"raw_text는 최대 {settings.max_input_chars}자까지 허용됩니다.",
        )

    extraction = extract_meeting(request.raw_text)

    db = get_firestore_client()
    doc_ref = db.collection(MEETINGS_COLLECTION).document()
    doc_ref.set(
        {
            **extraction.model_dump(),
            "raw_text": request.raw_text,
            "created_at": firestore_server_timestamp(),
        }
    )
    return MeetingExtractResponse(id=doc_ref.id, **extraction.model_dump())


@router.get("", response_model=list[MeetingSummary])
def list_meetings() -> list[MeetingSummary]:
    db = get_firestore_client()
    docs = (
        db.collection(MEETINGS_COLLECTION).order_by("created_at", direction="DESCENDING").stream()
    )
    return [MeetingSummary(id=doc.id, **doc.to_dict()) for doc in docs]


@router.get("/{meeting_id}", response_model=MeetingDetail)
def get_meeting(meeting_id: str) -> MeetingDetail:
    db = get_firestore_client()
    doc = db.collection(MEETINGS_COLLECTION).document(meeting_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="회의를 찾을 수 없습니다.")
    return MeetingDetail(id=doc.id, **doc.to_dict())


def firestore_server_timestamp():
    from firebase_admin import firestore

    return firestore.SERVER_TIMESTAMP
