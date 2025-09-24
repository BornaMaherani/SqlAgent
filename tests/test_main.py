import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base
from models import Sessions, Messages

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the database tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

def test_create_session(client, test_db):
    """Test creating a new session"""
    response = client.post(
        "/create-session",
        json={"session_id": 1, "name": "Test Session"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == 1
    assert data["name"] == "Test Session"

def test_get_session_info(client, test_db):
    """Test retrieving session information"""
    # First create a session
    client.post("/create-session", json={"session_id": 1, "name": "Test Session"})
    
    response = client.get("/show_sessions_info/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["session_id"] == 1

def test_get_nonexistent_session(client, test_db):
    """Test retrieving a non-existent session"""
    response = client.get("/show_sessions_info/999")
    assert response.status_code == 404

def test_delete_session(client, test_db):
    """Test deleting a session"""
    # First create a session
    client.post("/create-session", json={"session_id": 1, "name": "Test Session"})
    
    response = client.delete("/delete-session/1")
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_delete_nonexistent_session(client, test_db):
    """Test deleting a non-existent session"""
    response = client.delete("/delete-session/999")
    assert response.status_code == 404

if __name__ == "__main__":
    pytest.main()
