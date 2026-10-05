from fastapi import FastAPI

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