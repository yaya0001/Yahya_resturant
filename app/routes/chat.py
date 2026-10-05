from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.repositories.conversation_repo import ConversationRepository
from app.services.chat_service import ChatService
from app.services.conversations_memory import MemoryService


class ChatMessageRequest(BaseModel):
    conversation_id: str
    message: str
    user_id: str | None = None


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.get("", include_in_schema=False)
@router.get("/", include_in_schema=False)
def chat_root():
    return {
        "message": "Chat endpoints",
        "endpoints": [
            "/chat/message",
            "/chat/history/{conversation_id}",
        ],
    }


def get_chat_graph() -> Any:
    from app.core.config import settings

    if not settings.enable_chat_graph:
        return None

    if not settings.GROQ_API_KEY or settings.GROQ_API_KEY in {"", "YOUR_API_KEY"}:
        return None

    try:
        from app.ORC.state import app as graph
    except Exception:
        return None

    return graph


def get_chat_service(graph: Any = Depends(get_chat_graph)) -> ChatService:
    memory_service = MemoryService(ConversationRepository())
    return ChatService(memory_service=memory_service, graph=graph)


@router.post("/message")
def send_message(
    payload: ChatMessageRequest,
    service: ChatService = Depends(get_chat_service),
):
    user_id = payload.user_id or "anonymous"

    response = service.chat(
        conversation_id=payload.conversation_id,
        user_id=user_id,
        message=payload.message,
    )

    return {
        "conversation_id": payload.conversation_id,
        "user_id": user_id,
        "response": response,
    }


@router.get("/history/{conversation_id}")
def get_history(
    conversation_id: str,
    service: ChatService = Depends(get_chat_service),
):
    memory_service = service.memory_service
    try:
        history = memory_service.get_messages(conversation_id)
    except Exception:
        history = []

    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "role": message.type,
                "content": message.content,
            }
            for message in history
        ],
    }
