from app.repositories.conversation_repo import ConversationRepository


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