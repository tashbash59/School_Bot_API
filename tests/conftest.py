import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app, Base
from app.database import get_db
#from app.models import Base

# Тестовая база данных в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    # Создаем сессию
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Удаляем таблицы
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

# Фикстуры для тестовых данных
@pytest.fixture
def test_user_data():
    return {
        "telegram_id": 123456789,
        "username": "testuser",
        "full_name": "TASBASH",
        "role": "teacher"
    }

@pytest.fixture
def test_group_data():
    return {
        "name": "Test Group",
        "description": "Test description",
        "created_by": 0
    }

@pytest.fixture
def test_attachment_data():
    return {
        "homework_id": None, # Будет установлено в тесте
        "file_id": "string",
        "file_type": "text/plain",
        "file_name": "test.txt",
        "caption": "string",
    }

@pytest.fixture
def test_homework_data():
    return {
        "group_id": None,  # Будет установлено в тесте
        "assigned_by": 0,
        "title": "Test Homework",
        "description": "Test homework description",
        "deadline": "2024-12-31T23:59:59"
    }