from uuid import uuid4

from app.repositories.conversation_repo import ConversationRepository


def test_create_and_get_conversation():
    repository = ConversationRepository()

    conversation_id = str(uuid4())

    repository.create_conversation(
        conversation_id=conversation_id,
        user_id="test-user",
    )

    conversation = repository.get_conversation(
        conversation_id
    )

    assert conversation is not None
    assert conversation["conversation_id"] == conversation_id
    assert conversation["user_id"] == "test-user"