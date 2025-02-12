import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models.base import BaseModel
from config import Settings
from main import app
import os

# Test settings
class TestSettings(Settings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "test_user"
    DB_PASSWORD: str = "test_password"
    DB_NAME: str = "test_db"
    DEBUG: bool = True

    class Config:
        env_file = ".env.test"

@pytest.fixture(scope="session")
def test_settings():
    """Provides test configuration settings"""
    return TestSettings()

def get_test_db():
    """Get test database session"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def test_db_engine(test_settings):
    """Creates a test database engine"""
    engine = create_engine(
        test_settings.DATABASE_URL,
        pool_pre_ping=True,
        echo=test_settings.DEBUG
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

TestingSessionLocal = None

@pytest.fixture(scope="session", autouse=True)
def setup_test_db(test_db_engine):
    """Setup test database and session factory"""
    global TestingSessionLocal
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_db_engine
    )

@pytest.fixture(scope="function")
def test_db_session():
    """Provides a test database session"""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture(scope="function")
def test_base_model(test_db_session):
    """Provides a base model instance for testing"""
    model = BaseModel()
    test_db_session.add(model)
    test_db_session.commit()
    return model

@pytest.fixture(scope="function")
def client(test_db_session):
    """Test client fixture"""
    app.dependency_overrides[get_db] = lambda: test_db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
