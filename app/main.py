from fastapi import FastAPI

from app.routers import meetings

app = FastAPI(title="meeting-stt-app API")
app.include_router(meetings.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
