class ExportService:
    def export_csv(self, ctx, output_path: str):
        ctx.dataframe.to_csv(output_path, index=False)
