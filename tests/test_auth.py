import pytest
from fastapi import HTTPException
from jose import jwt
from main import SECRET_KEY, ALGORITHM, create_access_token, verify_password, get_current_user, pwd_context

def test_create_access_token():
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("sub") == "test@example.com"

def test_verify_password():
    plain_password = "testpassword123"
    hashed_password = pwd_context.hash(plain_password)
    assert verify_password(plain_password, hashed_password)
    assert not verify_password("wrongpassword", hashed_password)

def test_register_user(client):
    response = client.post(
        "/register/",
        params={"email": "newuser@example.com", "password": "newpassword123"}
    )
    assert response.status_code == 200
    assert "User registered successfully" in response.json()["message"]

def test_register_duplicate_user(client, test_user):
    response = client.post(
        "/register/",
        params={"email": test_user["email"], "password": "anotherpassword123"}
    )
    assert response.status_code == 409
    assert "User already exists" in response.json()["detail"]

def test_login_success(client, test_user):
    response = client.post(
        "/token",
        data={"username": test_user["email"], "password": test_user["password"]}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post(
        "/token",
        data={"username": "wrong@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]

def test_get_current_user(client, test_user_token, test_user):
    response = client.get(
        "/me/",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]

def test_get_current_user_invalid_token(client):
    response = client.get(
        "/me/",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert "Invalid token" in response.json()["detail"] 