from core.ingestao import load_csv, load_json
from core.contexto import DatasetContext
from core.analises import describe

class DatasetService:
    
    def load(self, file_path: str) -> DatasetContext:
        if file_path.endswith(".csv"):
            df = load_csv(file_path)
        elif file_path.endswith(".json"):
            df = load_json(file_path)
        else:
            raise ValueError("Formato de arquivo não suportado")

        name = file_path.split("/")[-1]

        # normalizar nomes das colunas pra facilitar o retorno via API
        df.columns = [c.replace('coluna_', '') for c in df.columns]

        return DatasetContext(
            name=name,
            dataframe=df
        )

    def list_columns(self, ctx: DatasetContext):
        return list(ctx.dataframe.columns)

    def summary(self, ctx: DatasetContext):
        return ctx.dataframe.describe()
