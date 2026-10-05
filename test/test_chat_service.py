from langchain_core.messages import AIMessage, HumanMessage

from app.services.chat_service import ChatService


class FakeMemoryService:
    def __init__(self):
        self.messages = {}

    def get_or_create_conversation(self, conversation_id: str, user_id: str):
        self.messages.setdefault(conversation_id, [])
        return {"conversation_id": conversation_id, "user_id": user_id}

    def get_messages(self, conversation_id: str, user_id: str | None = None):
        return [HumanMessage(content="hello")] + [
            HumanMessage(content=item["content"]) if item["role"] == "human" else AIMessage(content=item["content"])
            for item in self.messages.get(conversation_id, [])
        ]

    def add_message(self, conversation_id: str, role: str, content: str, user_id: str | None = None):
        self.messages.setdefault(conversation_id, []).append({"role": role, "content": content})


class FakeGraph:
    def invoke(self, payload):
        return {
            "messages": [
                HumanMessage(content="hello"),
                AIMessage(content="hi there"),
            ]
        }


def test_chat_service_is_compatible_with_service_contract():
    memory_service = FakeMemoryService()
    graph = FakeGraph()

    service = ChatService(memory_service=memory_service, graph=graph)
    response = service.chat(
        conversation_id="conv-1",
        user_id="user-1",
        message="hello",
    )

    assert response == "hi there"
    assert memory_service.messages["conv-1"][-1]["content"] == "hi there"
