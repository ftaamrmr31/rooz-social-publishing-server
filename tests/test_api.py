from unittest.mock import patch


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data


def test_api_root(client):
    response = client.get("/api/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_api_version(client):
    response = client.get("/api/version")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "0.1.0"


def test_create_user(client):
    response = client.post(
        "/api/users",
        json={"email": "test@example.com", "full_name": "Test User"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "created_at" in data


def test_create_user_duplicate_email(client):
    client.post(
        "/api/users",
        json={"email": "dup@example.com", "full_name": "User 1"},
    )
    response = client.post(
        "/api/users",
        json={"email": "dup@example.com", "full_name": "User 2"},
    )
    assert response.status_code == 400
    assert "Email already exists" in response.json()["detail"]


def test_list_users(client):
    client.post(
        "/api/users",
        json={"email": "a@example.com", "full_name": "A"},
    )
    client.post(
        "/api/users",
        json={"email": "b@example.com", "full_name": "B"},
    )
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_create_publish_job(client):
    response = client.post(
        "/api/publish",
        json={"platform": "telegram", "content": "Hello!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["platform"] == "telegram"
    assert data["content"] == "Hello!"
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data


def test_list_publish_jobs(client):
    client.post(
        "/api/publish",
        json={"platform": "telegram", "content": "Msg 1"},
    )
    client.post(
        "/api/publish",
        json={"platform": "twitter", "content": "Msg 2"},
    )
    response = client.get("/api/publish")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_telegram_send_now_no_token(client):
    """Without TELEGRAM_BOT_TOKEN configured, should return 400."""
    response = client.post(
        "/api/publish/telegram/send-now",
        json={"content": "Test message"},
    )
    assert response.status_code == 400
    assert "TELEGRAM_BOT_TOKEN" in response.json()["detail"]


def test_telegram_send_now_success(client):
    """With a mocked Telegram API call, should return success."""
    mock_response = {"ok": True, "result": {"message_id": 1}}
    with patch(
        "app.api.publish.send_telegram_message",
        return_value=mock_response,
    ):
        response = client.post(
            "/api/publish/telegram/send-now",
            json={"content": "Test message"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["platform"] == "telegram"
