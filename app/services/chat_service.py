from typing import Any

from langchain_core.messages import HumanMessage


class ChatService:

    def __init__(
        self,
        memory_service,
        graph,
    ):
        self.memory_service = memory_service
        self.graph = graph

    def _ensure_conversation(self, conversation_id: str, user_id: str):
        if hasattr(self.memory_service, "get_or_create_conversation"):
            return self.memory_service.get_or_create_conversation(
                conversation_id=conversation_id,
                user_id=user_id,
            )

        if hasattr(self.memory_service, "create_conversation"):
            return self.memory_service.create_conversation(
                conversation_id=conversation_id,
                user_id=user_id,
            )

        return None

    def _get_history(self, conversation_id: str, user_id: str):
        if hasattr(self.memory_service, "get_messages"):
            try:
                return self.memory_service.get_messages(
                    conversation_id=conversation_id,
                    user_id=user_id,
                )
            except TypeError:
                return self.memory_service.get_messages(conversation_id)

        return []

    def _add_message(self, conversation_id: str, user_id: str, role: str, content: str):
        if not hasattr(self.memory_service, "add_message"):
            return None

        try:
            return self.memory_service.add_message(
                conversation_id=conversation_id,
                user_id=user_id,
                role=role,
                content=content,
            )
        except TypeError:
            return self.memory_service.add_message(
                conversation_id=conversation_id,
                role=role,
                content=content,
            )

    def _extract_final_message(self, result: Any):
        if isinstance(result, dict):
            messages = result.get("messages", [])
        else:
            messages = result

        if not messages:
            raise ValueError("Graph response did not include any messages")

        final_message = messages[-1]
        return final_message.content if hasattr(final_message, "content") else str(final_message)

    def chat(
        self,
        conversation_id: str,
        user_id: str,
        message: str,
    ):
        if self.graph is None:
            return (
                "The chat service is currently unavailable. "
                "Configure the Groq/Hugging Face dependencies and credentials to enable AI responses."
            )

        try:
            self._ensure_conversation(
                conversation_id=conversation_id,
                user_id=user_id,
            )

            history = self._get_history(
                conversation_id=conversation_id,
                user_id=user_id,
            ) or []
        except Exception:
            history = []

        if not isinstance(history, list):
            history = list(history)

        history.append(HumanMessage(content=message))

        try:
            result = self.graph.invoke({"messages": history})
            final_message = self._extract_final_message(result)
        except Exception:
            return (
                "The AI chat graph is unavailable right now. "
                "Please check the Groq and model configuration."
            )

        try:
            self._add_message(
                conversation_id=conversation_id,
                user_id=user_id,
                role="human",
                content=message,
            )

            self._add_message(
                conversation_id=conversation_id,
                user_id=user_id,
                role="ai",
                content=final_message,
            )
        except Exception:
            pass

        return final_message