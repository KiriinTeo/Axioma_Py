class LoadDatasetUseCase:
    def __init__(self, dataset_service):
        self.dataset_service = dataset_service

    def execute(self, file_path: str):
        return self.dataset_service.load(file_path)
