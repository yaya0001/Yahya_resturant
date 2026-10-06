from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.repositories.conversation_repo import ConversationRepository
from app.routes.auth import get_current_user
from app.services.chat_service import ChatService
from app.services.conversations_memory import MemoryService


class ChatMessageRequest(BaseModel):
    message: str


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


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


@router.post("", status_code=status.HTTP_201_CREATED)
def create_conversation(
    current_user=Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    conversation_id = service.create_conversation(str(current_user.id))
    return {"conversation_id": conversation_id}


@router.get("")
def list_conversations(
    current_user=Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    conversations = service.list_conversations(str(current_user.id))
    return [
        {
            "conversation_id": conversation["conversation_id"],
            "updated_at": conversation.get("updated_at"),
            "messages": conversation.get("messages", []),
        }
        for conversation in conversations
    ]


@router.get("/{conversation_id}")
def get_history(
    conversation_id: str,
    current_user=Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    try:
        history = service.get_history(conversation_id, str(current_user.id))
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="Conversation not found") from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail="Forbidden") from exc

    return history


@router.post("/{conversation_id}/message")
def send_message(
    conversation_id: str,
    payload: ChatMessageRequest,
    current_user=Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    try:
        response = service.chat(
            conversation_id=conversation_id,
            user_id=str(current_user.id),
            message=payload.message,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="Conversation not found") from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail="Forbidden") from exc

    return {
        "conversation_id": conversation_id,
        "response": response,
    }


@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    current_user=Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    try:
        deleted = service.delete_conversation(conversation_id, str(current_user.id))
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="Conversation not found") from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail="Forbidden") from exc

    return {"deleted": deleted, "conversation_id": conversation_id}
