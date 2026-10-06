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

    def create_conversation(self, user_id: str) -> str:
        conversation_id = str(abs(hash(f"{user_id}:{__import__('uuid').uuid4()}")))
        self.memory_service.create_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )
        return conversation_id

    def list_conversations(self, user_id: str):
        return self.memory_service.get_user_conversations(user_id)

    def get_conversation(self, conversation_id: str, user_id: str):
        conversation = self.memory_service.get_conversation_for_user(
            conversation_id=conversation_id,
            user_id=user_id,
        )
        return {
            "conversation_id": conversation.get("conversation_id"),
            "messages": self.memory_service.dict_to_messages(
                conversation.get("messages", [])
            ),
        }

    def get_history(self, conversation_id: str, user_id: str):
        conversation = self.memory_service.get_conversation_for_user(
            conversation_id=conversation_id,
            user_id=user_id,
        )
        return {
            "conversation_id": conversation.get("conversation_id"),
            "messages": conversation.get("messages", []),
        }

    def delete_conversation(self, conversation_id: str, user_id: str):
        self.memory_service.get_conversation_for_user(
            conversation_id=conversation_id,
            user_id=user_id,
        )
        return self.memory_service.repository.delete_conversation(conversation_id)

    def chat(
        self,
        conversation_id: str,
        user_id: str,
        message: str,
    ):
        self.memory_service.get_conversation_for_user(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        history = self.memory_service.get_messages(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        history.append(HumanMessage(content=message))

        if self.graph is None:
            final_text = (
                "The chat service is currently unavailable. "
                "Configure the Groq/Hugging Face dependencies and credentials to enable AI responses."
            )
        else:
            result = self.graph.invoke({
                "messages": history,
                "conversation_id": conversation_id,
                "user_id": user_id,
            })
            final_message = result["messages"][-1]
            final_text = final_message.content

        self.memory_service.add_message(
            conversation_id=conversation_id,
            role="user",
            content=message,
        )

        self.memory_service.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=final_text,
        )

        return final_text