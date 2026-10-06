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

    def get_conversation_for_user(self, conversation_id: str, user_id: str):
        conversation = self.get_conversation(conversation_id)

        if conversation is None:
            raise LookupError(f"Conversation {conversation_id} not found")

        if str(conversation.get("user_id")) != str(user_id):
            raise PermissionError("You do not have access to this conversation")

        return conversation

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
            raise LookupError(f"Conversation {conversation_id} not found")

        if user_id is not None and str(conversation.get("user_id")) != str(user_id):
            raise PermissionError("You do not have access to this conversation")

        return self.dict_to_messages(conversation.get("messages", []))

    def get_user_conversations(self, user_id: str):
        conversations = self.repository.get_conversations_for_user(user_id)
        return [
            {
                "conversation_id": conversation.get("conversation_id"),
                "user_id": conversation.get("user_id"),
                "updated_at": conversation.get("updated_at"),
                "messages": conversation.get("messages", []),
            }
            for conversation in conversations
        ]

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