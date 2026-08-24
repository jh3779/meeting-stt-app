# ============================================================
# 담당: DB(Firestore) 연동
# meetings 컬렉션의 실제 문서 읽기/쓰기 로직은 여기가 아니라
# app/routers/meetings.py에 있음 — 이 파일은 연결(클라이언트) 설정만 담당.
# ============================================================
#
# 컬렉션 구조 (docs/ERD.md 1절 — 스키마를 바꾸면 ERD.md도 함께 수정할 것)
#   meetings/{documentId}
#     title: string, meeting_date: string, status: string, raw_text: string
#     decisions: array<string>
#     action_items: array<map{task, owner, deadline}>
#     created_at: timestamp (SERVER_TIMESTAMP)
#   위 필드는 app/schemas.py의 MeetingExtraction/MeetingDetail과 1:1로 맞춰져
#   있음 — 필드를 추가/변경하면 스키마·라우터·ERD.md 세 곳을 함께 고칠 것.
#
# 보안 요구사항 — Firestore 접근 경로 단일화 (PRD-MVP.md 4·6절, 필수)
#   - Firestore에 접근하는 코드는 반드시 이 모듈(get_firestore_client)을
#     거쳐야 한다. 클라이언트(client/)는 Firestore 주소·키를 아예 모르며,
#     항상 백엔드 API를 거쳐야 함 — 이 원칙을 절대 깨지 말 것.
#   - 서비스 계정 키(serviceAccountKey.json)는 백엔드 서버에만 존재하고
#     레포 루트에 두되 절대 커밋하지 않는다(.gitignore에 이미 등록됨).
#     실제 경로는 하드코딩하지 말고 Settings.firestore_service_account_path
#     (app/config.py, .env로 오버라이드 가능)로 가져올 것.
#
# 확장 시 참고 (MVP 범위 아님 — 지금 손대지 말 것)
#   - 인증(owner_uid)·PII 마스킹(raw_text_masked)·audit_logs 컬렉션은
#     docs/PRD-MAIN.md 3·4절, docs/ERD.md 4절 참고. MVP 단계에서는 미구현.
#   - action_items가 매우 많은 회의는 Firestore 문서 크기 제한(1MB)에
#     걸릴 수 있음(docs/ERD.md 5절 열린 질문) — MVP에서는 무시해도 됨.
#
# 로컬 에뮬레이터(토큰·클라우드 비용 없이 DB 로직만 테스트)
#   환경변수 FIRESTORE_EMULATOR_HOST가 설정돼 있으면(docker-compose.yml 참고)
#   실제 serviceAccountKey.json 없이 AnonymousCredentials로 에뮬레이터에 붙는다.
#   google.cloud.firestore.Client는 firebase_admin의 firestore.client()와
#   같은 API(.collection() 등)를 제공하므로 라우터 코드는 그대로 재사용 가능.

import os
from functools import lru_cache

import firebase_admin
from firebase_admin import credentials, firestore
from google.auth.credentials import AnonymousCredentials
from google.cloud import firestore as gcf

from app.config import get_settings

MEETINGS_COLLECTION = "meetings"


@lru_cache
def get_firestore_client():
    emulator_host = os.environ.get("FIRESTORE_EMULATOR_HOST")
    if emulator_host:
        return gcf.Client(project="demo-meeting-stt", credentials=AnonymousCredentials())

    settings = get_settings()
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.firestore_service_account_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()
