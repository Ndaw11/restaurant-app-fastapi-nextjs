from fastapi.testclient import TestClient
from backend.main import app
from backend.database import SessionLocal
from backend.models.user import User
from backend.utils.security import hash_password
import pytest

client = TestClient(app)


@pytest.fixture
def create_test_user():
    db = SessionLocal()
    user = User(
        email="admin@test.com",
        hashed_password=hash_password("admin123"),
        role="admin"
    )
    db.add(user)
    db.commit()
    yield user
    db.delete(user)
    db.commit()


def test_login_success(create_test_user):
    response = client.post(
        "/token",
        data={"username": "admin@test.com", "password": "admin123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure():
    response = client.post(
        "/token",
        data={"username": "wrong@test.com", "password": "wrongpass"}
    )
    assert response.status_code == 401


def test_protected_route_forbidden():
    response = client.get("/admin/users")  # pas de token
    assert response.status_code in [401, 403]
