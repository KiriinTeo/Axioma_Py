# from core.contexto import DatasetContext
# from infra.database.models.dataset import DatasetModel as Dataset
# from sqlalchemy.orm import Session

class LoadDatasetUseCase:
    def __init__(self, dataset_service, dataset_repo):
        self.dataset_service = dataset_service
        self.dataset_repo = dataset_repo

    def execute(self, file_path: str, user_id: str):
        ctx = self.dataset_service.load(file_path)

        dataset = self.dataset_repo.create(
            user_id=user_id,
            name=ctx.name
        )

        # enriquecendo metadados do contexto
        ctx.metadata = {
            "dataset_id": dataset.id,
            "user_id": user_id
        }

        return ctx, dataset.id
