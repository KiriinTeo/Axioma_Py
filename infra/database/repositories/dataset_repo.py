from infra.database.models.dataset import DatasetModel
from uuid import uuid4

class DatasetRepository:
    def __init__(self, db):
        self.db = db

    def create(self, user_id: str, name: str) -> str:
        dataset = DatasetModel(
            id=str(uuid4()),
            user_id=user_id,
            name=name
        )
        self.db.add(dataset)
        self.db.commit()
        self.db.refresh(dataset)

        return dataset.id

    def get_by_id(self, dataset_id: str, user_id: str) -> DatasetModel:
        return (
            self.db.query(DatasetModel)
            .filter(DatasetModel.id == dataset_id, DatasetModel.user_id == user_id)
            .first()
        )

    def list_by_user(self, user_id: str) -> DatasetModel:
        return (
            self.db.query(DatasetModel)
            .filter(DatasetModel.user_id == user_id)
            .all()
        )
