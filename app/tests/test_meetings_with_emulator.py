# DB(Firestore) 저장/조회 로직만 검증하는 테스트 — extract_meeting()은
# 픽스처 결과로 대체(monkeypatch)해서 OpenAI를 호출하지 않는다.
#
# 실행 전 준비: docker compose up -d (firestore-emulator)
#   FIRESTORE_EMULATOR_HOST가 안 잡혀 있으면 이 파일의 테스트는 스킵됨.

import json
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas import MeetingExtraction

FIXTURES_DIR = Path(__file__).parent / "fixtures"

requires_emulator = pytest.mark.skipif(
    "FIRESTORE_EMULATOR_HOST" not in os.environ,
    reason="FIRESTORE_EMULATOR_HOST 미설정 — docker compose up -d 로 에뮬레이터 먼저 실행",
)


@pytest.fixture
def sample_transcript() -> str:
    return (FIXTURES_DIR / "sample_meeting_transcript.txt").read_text(encoding="utf-8")


@pytest.fixture
def sample_extraction() -> MeetingExtraction:
    data = json.loads((FIXTURES_DIR / "sample_meeting_extraction.json").read_text(encoding="utf-8"))
    return MeetingExtraction(**data)


@requires_emulator
def test_extract_saves_and_lists(monkeypatch, sample_transcript, sample_extraction):
    monkeypatch.setattr(
        "app.routers.meetings.extract_meeting",
        lambda raw_text: sample_extraction,
    )
    client = TestClient(app)

    create_res = client.post("/meetings/extract", json={"raw_text": sample_transcript})
    assert create_res.status_code == 200
    assert create_res.json()["title"] == sample_extraction.title

    list_res = client.get("/meetings")
    assert list_res.status_code == 200
    titles = [m["title"] for m in list_res.json()]
    assert sample_extraction.title in titles

    meeting_id = next(m["id"] for m in list_res.json() if m["title"] == sample_extraction.title)
    detail_res = client.get(f"/meetings/{meeting_id}")
    assert detail_res.status_code == 200
    assert detail_res.json()["decisions"] == sample_extraction.decisions
