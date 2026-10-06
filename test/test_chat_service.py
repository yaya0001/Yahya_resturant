from types import SimpleNamespace

from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage, HumanMessage

from app.main import app
from app.routes import auth as auth_routes
from app.routes import chat as chat_routes
from app.services.chat_service import ChatService
from app.services.conversations_memory import MemoryService


class FakeMemoryService:
    def __init__(self):
        self.messages = {}

    def get_or_create_conversation(self, conversation_id: str, user_id: str):
        self.messages.setdefault(conversation_id, [])
        return {"conversation_id": conversation_id, "user_id": user_id}

    def get_conversation_for_user(self, conversation_id: str, user_id: str):
        return {"conversation_id": conversation_id, "user_id": user_id, "messages": []}

    def get_messages(self, conversation_id: str, user_id: str | None = None):
        return [HumanMessage(content="hello")] + [
            HumanMessage(content=item["content"]) if item["role"] == "human" else AIMessage(content=item["content"])
            for item in self.messages.get(conversation_id, [])
        ]

    def add_message(self, conversation_id: str, role: str, content: str, user_id: str | None = None):
        self.messages.setdefault(conversation_id, []).append({"role": role, "content": content})

    def get_user_conversations(self, user_id: str):
        return [{"conversation_id": "conv-1", "user_id": user_id, "updated_at": "2026-10-06T00:00:00", "messages": []}]


class FakeGraph:
    def invoke(self, payload):
        return {
            "messages": [
                HumanMessage(content="hello"),
                AIMessage(content="hi there"),
            ]
        }


class FakeRepo:
    def __init__(self):
        self.data = {
            "conv-1": {
                "conversation_id": "conv-1",
                "user_id": "10",
                "messages": [
                    {"role": "user", "content": "hello"},
                    {"role": "assistant", "content": "hi"},
                ],
            }
        }

    def get_conversation(self, conversation_id):
        return self.data.get(conversation_id)

    def get_conversations_for_user(self, user_id):
        return [
            conversation for conversation in self.data.values()
            if str(conversation["user_id"]) == str(user_id)
        ]

    def create_conversation(self, conversation_id, user_id):
        self.data[conversation_id] = {"conversation_id": conversation_id, "user_id": str(user_id), "messages": []}
        return self.data[conversation_id]

    def add_message(self, conversation_id, role, content):
        self.data.setdefault(conversation_id, {"conversation_id": conversation_id, "user_id": "0", "messages": []})
        self.data[conversation_id]["messages"].append({"role": role, "content": content})

    def delete_conversation(self, conversation_id):
        return self.data.pop(conversation_id, None) is not None


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


def test_memory_service_rejects_other_user_access():
    memory_service = MemoryService(FakeRepo())

    try:
        memory_service.get_messages("conv-1", user_id="20")
        raise AssertionError("PermissionError was expected for a different user")
    except PermissionError:
        pass


def test_chat_route_uses_authenticated_user_and_url_conversation_id():
    class FakeChatService:
        def create_conversation(self, user_id):
            return f"conv-{user_id}"

        def list_conversations(self, user_id):
            return [{"conversation_id": f"conv-{user_id}", "updated_at": "2026-10-06T00:00:00", "messages": []}]

        def get_history(self, conversation_id, user_id):
            return {"conversation_id": conversation_id, "messages": []}

        def chat(self, conversation_id, user_id, message):
            assert user_id == "7"
            assert conversation_id == "conv-7"
            return "hello there"

        def delete_conversation(self, conversation_id, user_id):
            return True

    fake_user = SimpleNamespace(id=7, name="Alice", mail="alice@example.com")
    app.dependency_overrides[auth_routes.get_current_user] = lambda: fake_user
    app.dependency_overrides[chat_routes.get_chat_service] = lambda: FakeChatService()

    try:
        client = TestClient(app)
        response = client.post("/chat", json={})
        assert response.status_code == 201
        assert response.json() == {"conversation_id": "conv-7"}

        list_response = client.get("/chat")
        assert list_response.status_code == 200

        message_response = client.post(
            "/chat/conv-7/message",
            json={"message": "hello"},
        )
        assert message_response.status_code == 200
        assert message_response.json()["response"] == "hello there"
    finally:
        app.dependency_overrides.clear()
