from core.contexto import DatasetContext

def export_csv(ctx: DatasetContext, path: str):
    ctx.dataframe.to_csv(path, index=False)
