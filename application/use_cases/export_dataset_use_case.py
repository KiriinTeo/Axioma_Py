class ExportDatasetUseCase:
    def __init__(self, export_service):
        self.export_service = export_service

    def execute(self, ctx, output_path: str):
        self.export_service.export_csv(ctx, output_path)
