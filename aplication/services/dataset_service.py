from core.ingestao import load_csv, load_json
from core.contexto import DatasetContext

class DatasetService:
    def load(self, file_path: str):
        if file_path.endswith(".csv"):
            df = load_csv(file_path)
        elif file_path.endswith(".json"):
            df = load_json(file_path)
        else:
            raise ValueError("Formato de arquivo não suportado")

        return DatasetContext(df)

    def list_columns(self, ctx: DatasetContext):
        return list(ctx.dataframe.columns)

    def summary(self, ctx: DatasetContext):
        return ctx.dataframe.describe()
