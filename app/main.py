from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import meetings

app = FastAPI(title="meeting-stt-app API")

# 클라이언트(client/)는 빌드 없는 정적 HTML이라 file://나 별도 포트의 정적
# 서버에서 열림 — 인증이 없는 MVP 데모용 API라 모든 출처를 허용한다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meetings.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
