from core.contexto import DatasetContext
from infra.database.models.dataset import DatasetModel as Dataset

class LoadDatasetUseCase:
    from sqlalchemy.orm import Session
    
    def __init__(self, dataset_service):
        self.dataset_service = dataset_service

    def execute(self, file_path: str, user_id: str, db: Session):
        df = self.dataset_service.load(file_path)

        dataset = Dataset(
            name=file_path,
            user_id=user_id
        )

        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        return DatasetContext(
            name=file_path,
            dataframe=df,
            dataset_id=dataset.id
        )
