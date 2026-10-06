from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.routes.auth import router as auth_router
from app.routes.booking import router as booking_router
from app.routes.chat import router as chat_router


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="NovaBite restaurant assistant API",
)


app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(booking_router)

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": settings.app_name.lower(),
        "environment": settings.app_env,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ui")
def ui_page():
    return FileResponse(str(BASE_DIR / "static" / "chat_tester.html"))