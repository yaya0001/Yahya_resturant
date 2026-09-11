from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=f"{settings.app_name} Multi-Agent API",
    version="0.1.0",
)


@app.get("/")
async def health_check():
    return {
        "status": "ok",
        "service": settings.app_name.lower(),
        "environment": settings.app_env,
    }