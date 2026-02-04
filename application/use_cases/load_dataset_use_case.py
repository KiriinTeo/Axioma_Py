# from core.contexto import DatasetContext
# from infra.database.models.dataset import DatasetModel as Dataset
# from sqlalchemy.orm import Session

class LoadDatasetUseCase:
    def __init__(self, dataset_service):
        self.dataset_service = dataset_service

    def execute(self, file_path: str, user_id: str, dataset_repo):
        ctx = self.dataset_service.load(file_path)

        dataset_id = dataset_repo.create(
            user_id=user_id,
            name=ctx.name,
        )
        
        # enriquecendo metadados do contexto
        ctx.metadata = {
            "dataset_id": dataset_id,
            "user_id": user_id,
            "rows": ctx.dataframe.shape[0],
            "columns": ctx.dataframe.shape[1],
            "schema": {col: str(dtype) for col, dtype in zip(ctx.dataframe.columns, ctx.dataframe.dtypes)}
        }

        return ctx, dataset_id

        
        

        
