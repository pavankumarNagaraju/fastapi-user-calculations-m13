# FILE: tests/test_users_integration.py
import time
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login_user():
    # unique email each run
    email = f"user{int(time.time())}@test.com"

    # Register
    register_resp = client.post(
        "/users/register",
        json={
            "email": email,
            "full_name": "Test User",
            "password": "secret123",
        },
    )
    assert register_resp.status_code == 201
    data = register_resp.json()
    assert data["email"] == email
    assert "id" in data

    # Login
    login_resp = client.post(
        "/users/login",
        json={"email": email, "password": "secret123"},
    )
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert login_data["message"] == "Login successful"
    assert login_data["user_id"] == data["id"]
