from datetime import datetime, timezone

from app.database.mongo import conversations_collection


class ConversationRepository:

    def get_conversation(self, conversation_id: str):
        return conversations_collection.find_one(
            {"conversation_id": conversation_id}
        )

    def get_conversations_for_user(self, user_id: str):
        return list(
            conversations_collection.find({"user_id": str(user_id)})
            .sort("updated_at", -1)
        )

    def create_conversation(
        self,
        conversation_id: str,
        user_id: str,
    ):
        document = {
            "conversation_id": conversation_id,
            "user_id": str(user_id),
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

    def delete_conversation(self, conversation_id: str):
        result = conversations_collection.delete_one({"conversation_id": conversation_id})
        return result.deleted_count > 0