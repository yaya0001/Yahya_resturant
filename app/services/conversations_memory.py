from app.repositories.conversation_repo import ConversationRepository
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage


class MemoryService:

    def __init__(self, repository: ConversationRepository):
        self.repository = repository

    def get_conversation(self, conversation_id: str):
        return self.repository.get_conversation(conversation_id)

    def get_or_create_conversation(
        self,
        conversation_id: str,
        user_id: str,
    ):
        conversation = self.get_conversation(conversation_id)
        if conversation is not None:
            return conversation

        return self.create_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

    def create_conversation(
        self,
        conversation_id: str,
        user_id: str,
    ):
        return self.repository.create_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        user_id: str | None = None,
    ):
        return self.repository.add_message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

    def message_to_dict(self, message: BaseMessage) -> dict:
        if isinstance(message, HumanMessage):
            role = "user"
        elif isinstance(message, AIMessage):
            role = "assistant"
        else:
            raise ValueError(
                f"Unsupported message type: {type(message)}"
            )

        return {
            "role": role,
            "content": message.content,
        }

    def dict_to_messages(self, messages_dict: list[dict]) -> list[BaseMessage]:
        messages = []
        for message_dict in messages_dict:
            role = message_dict["role"]
            content = message_dict["content"]

            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))

        return messages

    def get_messages(
        self,
        conversation_id: str,
        user_id: str | None = None,
    ):
        conversation = self.repository.get_conversation(conversation_id)

        if conversation is None:
            if user_id is not None:
                self.create_conversation(
                    conversation_id=conversation_id,
                    user_id=user_id,
                )
            return []

        return self.dict_to_messages(conversation.get("messages", []))

    def save_message(
        self,
        conversation_id: str,
        message: BaseMessage,
    ):
        data = self.message_to_dict(message)

        self.repository.add_message(
            conversation_id=conversation_id,
            role=data["role"],
            content=data["content"],
        )