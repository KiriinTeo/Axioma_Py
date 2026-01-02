class DatasetSummaryUseCase:
    def __init__(self, dataset_service):
        self.dataset_service = dataset_service

    def execute(self, ctx):
        return self.dataset_service.summary(ctx).to_dict()
