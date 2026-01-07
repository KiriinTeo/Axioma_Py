class ListColumnsUseCase:
    def __init__(self, dataset_service, dataset_repo):
        self.dataset_service = dataset_service
        self.dataset_repo = dataset_repo

    def execute(self, ctx, user_id: str):
        columns = self.dataset_service.list_columns(ctx)
        
        dataset = self.dataset_repo.create(
            user_id=user_id,
            name=ctx.name
        )

        ctx.metadata = {
            "dataset_id": dataset.id,
            "user_id": user_id
        }
        
        return columns, dataset.id