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
        return dataset.id
