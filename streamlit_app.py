# Streamlit Cloud(share.streamlit.io) 데모용 진입점.
#
# FastAPI 백엔드(app/main.py)와는 별개의 배포 대상 — Streamlit Cloud는
# `streamlit run <file>.py` 형태만 실행하므로, HTTP 계층(app/routers/)을
# 거치지 않고 서비스 계층(app/services/)을 직접 호출한다. app/routers/meetings.py가
# 하던 일(추출 → Firestore 저장, 목록 조회)을 이 파일이 대신 조립할 뿐,
# 실제 로직(추출 체인·Firestore 접근)은 그대로 재사용 — 로직 중복 없음.
#
# 로컬 실행: streamlit run streamlit_app.py
# (.env의 OPENAI_API_KEY/FIRESTORE_EMULATOR_HOST 등을 app.config가 그대로 읽음)
#
# Streamlit Cloud 배포: 앱 설정 → Secrets에 아래 형식으로 채울 것
# (.streamlit/secrets.toml.example 참고, 이 파일 자체는 절대 커밋하지 말 것):
#   OPENAI_API_KEY = "..."
#   [firestore_service_account]
#   ... serviceAccountKey.json 내용 그대로 ...

import json
import os
import tempfile

import streamlit as st

try:
    _secrets = dict(st.secrets)
except Exception:
    _secrets = {}

if "firestore_service_account" in _secrets:
    _cred_file = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(dict(_secrets.pop("firestore_service_account")), _cred_file)
    _cred_file.close()
    os.environ.setdefault("FIRESTORE_SERVICE_ACCOUNT_PATH", _cred_file.name)

for _key, _value in _secrets.items():
    os.environ.setdefault(_key, str(_value))

from app.schemas import ActionItem  # noqa: E402
from app.services.firestore_client import (  # noqa: E402
    MEETINGS_COLLECTION,
    SERVER_TIMESTAMP,
    get_firestore_client,
)
from app.services.my_service_structured import extract_meeting  # noqa: E402

st.set_page_config(page_title="회의록 STT 요약 (데모)", page_icon="📝")
st.title("회의록 STT 요약 서비스 — 데모")
st.caption("STT 텍스트 → LLM 구조화 추출 → Firestore 저장·조회 (LG CNS AI Campus 미니 프로젝트)")

tab_extract, tab_list = st.tabs(["새 회의록", "회의 목록"])

with tab_extract:
    raw_text = st.text_area(
        "STT 텍스트 붙여넣기",
        height=300,
        max_chars=20_000,
        placeholder="회의 녹취 텍스트를 붙여넣으세요.",
    )
    if st.button("추출 및 저장", type="primary"):
        if not raw_text.strip():
            st.error("텍스트를 입력하세요.")
        else:
            with st.spinner("추출 중..."):
                try:
                    extraction = extract_meeting(raw_text)
                    db = get_firestore_client()
                    doc_ref = db.collection(MEETINGS_COLLECTION).document()
                    doc_ref.set(
                        {
                            **extraction.model_dump(),
                            "raw_text": raw_text,
                            "created_at": SERVER_TIMESTAMP,
                        }
                    )
                    st.success(f"저장 완료 (id: {doc_ref.id})")
                    st.subheader(extraction.title)
                    st.write(f"{extraction.meeting_date} · {extraction.status}")
                    st.write("**결정사항**")
                    for decision in extraction.decisions:
                        st.write(f"- {decision}")
                    st.write("**액션아이템**")
                    if extraction.action_items:
                        st.table(
                            [
                                {
                                    "할 일": item.task,
                                    "담당자": item.owner,
                                    "기한": item.deadline or "-",
                                }
                                for item in extraction.action_items
                            ]
                        )
                    else:
                        st.caption("액션아이템이 없습니다.")
                except Exception as e:  # noqa: BLE001 — 데모 UI, 원인 그대로 노출
                    st.error(f"오류: {e}")

with tab_list:
    if st.button("새로고침"):
        st.rerun()
    try:
        db = get_firestore_client()
        docs = list(
            db.collection(MEETINGS_COLLECTION)
            .order_by("created_at", direction="DESCENDING")
            .stream()
        )
        if not docs:
            st.caption("저장된 회의가 없습니다.")
        for doc in docs:
            data = doc.to_dict()
            with st.expander(
                f"{data.get('title')} — {data.get('meeting_date')} [{data.get('status')}]"
            ):
                st.write("**결정사항**")
                for decision in data.get("decisions", []):
                    st.write(f"- {decision}")
                st.write("**액션아이템**")
                items = [ActionItem(**item) for item in data.get("action_items", [])]
                if items:
                    st.table(
                        [
                            {"할 일": item.task, "담당자": item.owner, "기한": item.deadline or "-"}
                            for item in items
                        ]
                    )
                else:
                    st.caption("액션아이템이 없습니다.")
    except Exception as e:  # noqa: BLE001 — 데모 UI, 원인 그대로 노출
        st.error(f"목록을 불러오지 못했습니다: {e}")
