from datetime import datetime, timezone

from app.database.mongo import conversations_collection


class ConversationRepository:

    def get_conversation(self, conversation_id: str):
        return conversations_collection.find_one(
            {"conversation_id": conversation_id}
        )

    def create_conversation(
        self,
        conversation_id: str,
        user_id: str,
    ):
        document = {
            "conversation_id": conversation_id,
            "user_id": user_id,
            "messages": [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

        conversations_collection.insert_one(document)

        return document

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ):
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now(timezone.utc),
        }

        conversations_collection.update_one(
            {"conversation_id": conversation_id},
            {
                "$push": {"messages": message},
                "$set": {
                    "updated_at": datetime.now(timezone.utc)
                },
            },
        )