import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.main import app
from infra.database.base import Base
from api.dependencies.db import get_db

# =========================
# Database de teste (isolada)
# =========================

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =========================
# Fixtures globais
# =========================

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

class TestAuth:

    def test_register_user(self, client):
        res = client.post("/auth/register", json={
            "email": "test@example.com",
            "password": "123456"
        })

        assert res.status_code == 200
        assert "user_id" in res.json()

    def test_login_user(self, client):
        client.post("/auth/register", json={
            "email": "login@example.com",
            "password": "123456"
        })

        res = client.post("/auth/login", json={
            "email": "login@example.com",
            "password": "123456"
        })

        body = res.json()
        assert res.status_code == 200
        assert "access_token" in body

class TestDataset:

    def test_load_dataset(self, client):
        token = self._auth(client)

        res = client.post(
            "/dataset/load",
            params={"path": "data/exemplo.csv"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert res.status_code == 200
        assert "dataset_id" in res.json()

    def _auth(self, client):
        client.post("/auth/register", json={
            "email": "ds@example.com",
            "password": "123456"
        })

        res = client.post("/auth/login", json={
            "email": "ds@example.com",
            "password": "123456"
        })

        return res.json()["access_token"]

class TestStats:

    def test_summary(self, client):
        token = self._prepare_dataset(client)

        res = client.get(
            "/stats/1/summary",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert res.status_code == 200
        assert "summary" in res.json()

    def _prepare_dataset(self, client):
        client.post("/auth/register", json={
            "email": "stats@example.com",
            "password": "123456"
        })

        login = client.post("/auth/login", json={
            "email": "stats@example.com",
            "password": "123456"
        })

        token = login.json()["access_token"]

        client.post(
            "/dataset/load",
            params={"path": "data/exemplo.csv"},
            headers={"Authorization": f"Bearer {token}"}
        )

        return token

