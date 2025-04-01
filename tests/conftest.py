import os
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from main import app, get_db

# Mock environment variables
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["SMTP_SERVER"] = "localhost"
os.environ["SMTP_PORT"] = "587"
os.environ["SMTP_EMAIL"] = "test@example.com"
os.environ["SMTP_PASSWORD"] = "test_password"
os.environ["CLOUDINARY_CLOUD_NAME"] = "test_cloud"
os.environ["CLOUDINARY_API_KEY"] = "test_key"
os.environ["CLOUDINARY_API_SECRET"] = "test_secret"

# Create a test database in memory
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Store for test fixtures
test_state = {}

@pytest.fixture(autouse=True)
def mock_smtp():
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        test_state['mock_smtp'] = mock_server
        yield mock_server

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(client):
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/register/", params=user_data)
    assert response.status_code == 200
    
    # Get the verification token from the mock SMTP server
    mock_smtp = test_state['mock_smtp']
    verification_token = mock_smtp.send_message.call_args[0][0].get_content().split("/verify/")[1].strip()
    
    # Verify the user
    response = client.get(f"/verify/{verification_token}")
    assert response.status_code == 200
    
    return user_data

@pytest.fixture
def test_user_token(client, test_user):
    response = client.post("/token", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    return response.json()["access_token"] 