import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.main import app
from infra.database.base import Base
from api.dependencies.deps import get_db

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
    
    def test_health(self, client):
        res = client.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "saudavel"


class TestDataset:

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
    
    def test_load_dataset(self, client):
        token = self._auth(client)

        res = client.post(
            "/dataset/load",
            params={"path": "data/exemplo.csv"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert res.status_code == 200
        assert "dataset_id" in res.json()

    def test_list_datasets(self, client):
        token = self._auth(client)

        client.post(
            "/dataset/load",
            params={"path": "data/exemplo.csv"},
            headers={"Authorization": f"Bearer {token}"}
        )

        res = client.get(
            "/dataset",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert res.status_code == 200
        assert isinstance(res.json(), list)
        assert len(res.json()) >= 1

    def test_delete_dataset(self, client):
        token = self._auth(client)

        load_res = client.post(
            "/dataset/load",
            params={"path": "data/exemplo.csv"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert load_res.status_code == 200
        dataset_id = load_res.json()["dataset_id"]

        del_res = client.delete(
            f"/dataset/{dataset_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert del_res.status_code == 200

        list_res = client.get(
            "/dataset",
            headers={"Authorization": f"Bearer {token}"}
        )

        datasets = list_res.json()
        assert all(d["id"] != dataset_id for d in datasets)

    def test_rename_dataset(self, client):
        token = self._auth(client)

        load_res = client.post(
            "/dataset/load",
            params={"path": "data/exemplo.csv"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert load_res.status_code == 200
        dataset_id = load_res.json()["dataset_id"]

        new_name = "Novo Nome do Dataset"
        rename_res = client.patch(
            f"/dataset/{dataset_id}/rename",
            json={"new_name": new_name},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert rename_res.status_code == 200
        assert rename_res.json()["name"] == new_name

        list_res = client.get(
            "/dataset",
            headers={"Authorization": f"Bearer {token}"}
        )

        datasets = list_res.json()
        renamed_dataset = next((d for d in datasets if d["id"] == dataset_id), None)
        assert renamed_dataset is not None
        assert renamed_dataset["name"] == new_name
    
    def test_export_dataset(self, client):
        token = self._auth(client)

        load_res = client.post(
            "/dataset/load",
            params={"path": "data/exemplo.csv"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert load_res.status_code == 200
        dataset_id = load_res.json()["dataset_id"]

        export_path = "data/exported_exemplo.csv"
        export_res = client.post(
            "/export/to_csv",
            params={"dataset_id": dataset_id, "path": export_path},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert export_res.status_code == 200
        assert export_res.json()["status"] == "exported"
        assert export_res.json()["path"] == export_path

class TestStats:

    def test_summary(self, client):
        token = self._auth(client)

        load_res = client.post(
            "/dataset/load",
            params={"path": "data/exemplo.csv"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert load_res.status_code == 200
        dataset_id = load_res.json()["dataset_id"]

        res = client.get(
            f"/stats/{dataset_id}/summary",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert res.status_code == 200
        assert "summary" in res.json()
    
    def test_list_columns(self, client):
        token = self._auth(client)

        load_res = client.post(
            "/dataset/load",
            params={"path": "data/exemplo.csv"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert load_res.status_code == 200
        dataset_id = load_res.json()["dataset_id"]

        res = client.get(
            f"/dataset/{dataset_id}/columns",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert res.status_code == 200
        assert "columns" in res.json()
        assert isinstance(res.json()["columns"], list) 

    def test_basic_analysis(self, client):
        token = self._auth(client)

        load_res = client.post(
            "/dataset/load",
            params={"path": "data/exemplo.csv"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert load_res.status_code == 200
        dataset_id = load_res.json()["dataset_id"]

        res = client.get(
            f"/stats/{dataset_id}/analysis",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert res.status_code == 200
        assert "analysis" in res.json()

    def test_apply_filter(self, client):
        token = self._prepare_dataset(client)

        load_res = client.post(
            "/dataset/load",
            params={"path": "data/exemplo.csv"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert load_res.status_code == 200
        dataset_id = load_res.json()["dataset_id"]

        filter_res = client.post(
            "/filter/apply",
            json={
                "dataset_id": dataset_id,
                "column": "x",
                "operator": "<",
                "value": 5
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        assert filter_res.status_code == 200
        assert "dataset_id" in filter_res.json()
    
    def test_plot_generation(self, client):
        token = self._prepare_dataset(client)

        load_res = client.post(
            "/dataset/load",
            params={"path": "data/exemplo.csv"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert load_res.status_code == 200
        dataset_id = load_res.json()["dataset_id"]

        plot_res = client.post(
            "/plot/generate",
            json={
                "dataset_id": dataset_id,
                "plot_type": "scatter",
                "x": "x",
                "y": "y"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        assert plot_res.status_code == 200
        assert "image" in plot_res.json()
    
    def _auth(self, client):
        client.post("/auth/register", json={
            "email": "stats@example.com",
            "password": "123456"
        })

        res = client.post("/auth/login", json={
            "email": "stats@example.com",
            "password": "123456"
        })

        return res.json()["access_token"]

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

