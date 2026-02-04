import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
from uuid import uuid4

from api.main import app
from infra.database.base import Base
from api.dependencies.deps import get_db
from infra.database.models.filter import FilterModel
from infra.database.models.plot import PlotModel
from infra.database.models.export import ExportModel
from infra.database.models.analysis import AnalysisModel


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
            "password": "123456",
            "id": "1"
        })

        print(res.status_code)
        print(res.json())

        assert res.status_code == 200
        assert "user_id" in res.json()

    def test_login_user(self, client):
        client.post("/auth/register", json={
            "email": "login@example.com",
            "password": "123456",
            "id": "1"
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
            "password": "123456",
            "id": "1"
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

        load_res = client.post(
            "/dataset/load",
            params={"path": "data/exemplo.csv"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert load_res.status_code == 200

        res = client.get(
            "/dataset",
            headers={"Authorization": f"Bearer {token}"}
        )

        datasets = res.json()
        assert isinstance(datasets, list)
        assert len(datasets) >= 1

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

        get_res = client.get(
            "/dataset",
            headers={"Authorization": f"Bearer {token}"}
        )

        datasets = get_res.json()
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

        rename_res = client.patch(
            f"/dataset/{dataset_id}/rename",
            json={"new_name": "Novo Nome"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert rename_res.status_code == 200

        get_res = client.get(
            "/dataset",
            headers={"Authorization": f"Bearer {token}"}
        )

        datasets = get_res.json()
        renamed = next((d for d in datasets if d["id"] == dataset_id), None)
        assert renamed is not None
        assert renamed["name"] == "Novo Nome"

    def test_export_dataset(self, client):
        token = self._auth(client)

        load_res = client.post(
            "/dataset/load",
            params={"path": "data/exemplo.csv"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert load_res.status_code == 200
        dataset_id = load_res.json()["dataset_id"]

        export_res = client.post(
            "/export/to_csv",
            params={
                "dataset_id": dataset_id,
                "path": "data/test_export.csv"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        assert export_res.status_code == 200
        assert export_res.json()["status"] == "exported"


class TestPersistence:

    def test_filter_creation(self, db):
        record = FilterModel(
            id=str(uuid4()),
            user_id=1,
            dataset_id="dataset_123",
            column_name="categoria",
            operator="=",
            value="ativo"
        )
        db.add(record)
        db.commit()

        result = db.query(FilterModel).first()
        assert result is not None
        assert result.column_name == "categoria"
        assert result.operator == "="
        assert result.value == "ativo"

    def test_filter_timestamp(self, db):
        record = FilterModel(
            id=str(uuid4()),
            user_id=1,
            dataset_id="dataset_123",
            column_name="status",
            operator="!=",
            value="inativo"
        )
        db.add(record)
        db.commit()

        result = db.query(FilterModel).first()
        assert result.created_at is not None
        assert isinstance(result.created_at, datetime)


    def test_plot_creation(self, db):
        record = PlotModel(
            id=str(uuid4()),
            user_id=1,
            dataset_id="dataset_123",
            plot_type="bar",
            x_axis="categoria",
            y_axis="valor"
        )
        db.add(record)
        db.commit()

        result = db.query(PlotModel).first()
        assert result is not None
        assert result.plot_type == "bar"

    def test_multiple_plots(self, db):
        for plot_type in ["bar", "pie", "line"]:
            db.add(
                PlotModel(
                    id=str(uuid4()),
                    user_id=1,
                    dataset_id="dataset_123",
                    plot_type=plot_type,
                    x_axis="x",
                    y_axis="y"
                )
            )
        db.commit()

        results = db.query(PlotModel).all()
        assert len(results) == 3


    def test_export_creation(self, db):
        record = ExportModel(
            id=str(uuid4()),
            user_id=1,
            dataset_id="dataset_123",
            file_path="/exports/data.csv",
            file_format="csv"
        )
        db.add(record)
        db.commit()

        result = db.query(ExportModel).first()
        assert result is not None
        assert result.file_format == "csv"
        assert result.created_at is not None

    def test_export_audit_trail(self, db):
        for i in range(3):
            db.add(
                ExportModel(
                    id=str(uuid4()),
                    user_id=1,
                    dataset_id="dataset_123",
                    file_path=f"/exports/export_{i}.csv",
                    file_format="csv"
                )
            )
        db.commit()

        exports = db.query(ExportModel).all()
        assert len(exports) == 3
        assert exports[0].created_at <= exports[-1].created_at

    def test_analysis_creation(self, db):
        record = AnalysisModel(
            id=str(uuid4()),
            user_id=1,
            dataset_id="dataset_123",
            analysis_type="summary",
            result='{"mean": 10}'
        )
        db.add(record)
        db.commit()

        result = db.query(AnalysisModel).first()
        assert result is not None
        assert result.analysis_type == "summary"
        assert "mean" in result.result

    def test_multiple_analysis_types(self, db):
        for analysis_type in ["summary", "basic", "performance"]:
            db.add(
                AnalysisModel(
                    id=str(uuid4()),
                    user_id=1,
                    dataset_id="dataset_123",
                    analysis_type=analysis_type,
                    result=f'{{"type": "{analysis_type}"}}'
                )
            )
        db.commit()

        results = db.query(AnalysisModel).all()
        types = {r.analysis_type for r in results}
        assert {"summary", "basic", "performance"} <= types

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
            "password": "123456",
            "id": "1"
        })

        res = client.post("/auth/login", json={
            "email": "stats@example.com",
            "password": "123456"
        })

        return res.json()["access_token"]

    def _prepare_dataset(self, client):
        client.post("/auth/register", json={
            "email": "stats@example.com",
            "password": "123456",
            "id": "1"
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

