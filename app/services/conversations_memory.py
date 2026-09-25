from app.repositories.conversation_repo import ConversationRepository
from langchain_core.messages import HumanMessage, AIMessage


class MemoryService:

    def __init__(self, repository: ConversationRepository):
        self.repository = repository

    def get_conversation(self, conversation_id: str):
        return self.repository.get_conversation(conversation_id)

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
    ):
        return self.repository.add_message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )


    def load_messages(conversation):
        messages = []

        for message in conversation["messages"]:

            if message["role"] == "user":
                messages.append(
                    HumanMessage(
                        content=message["content"]
                    )
                )

            elif message["role"] == "assistant":
                messages.append(
                    AIMessage(
                        content=message["content"]
                    )
                )

        return messages