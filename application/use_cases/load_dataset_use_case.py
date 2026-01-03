class LoadDatasetUseCase:
    from sqlalchemy.orm import Session

    def __init__(self, dataset_service):
        self.dataset_service = dataset_service

    def execute(self, file_path: str, user_id: str, db: Session):
        return self.dataset_service.load(file_path, user_id, db)