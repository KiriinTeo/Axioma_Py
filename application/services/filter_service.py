from core.contexto import DatasetContext


class FilterService:
    def apply(self, ctx: DatasetContext, column: str, operator: str, value):
        df = ctx.dataframe

        if operator == "==":
            filtered = df[df[column] == value]
        elif operator == ">":
            filtered = df[df[column] > value]
        elif operator == "<":
            filtered = df[df[column] < value]
        else:
            raise ValueError("Operador não suportado")

        # preserve context name and metadata when creating new context
        new_ctx = DatasetContext(
            name=ctx.name,
            dataframe=filtered,
            metadata={**(ctx.metadata or {}), "rows": int(filtered.shape[0]), "columns": int(filtered.shape[1])}
        )

        return new_ctx
