import core.contexto as DatasetContext

class FilterService:
    def apply(self, ctx, column: str, operator: str, value):
        df = ctx.dataframe

        if operator == "==":
            filtered = df[df[column] == value]
        elif operator == ">":
            filtered = df[df[column] > value]
        elif operator == "<":
            filtered = df[df[column] < value]
        else:
            raise ValueError("Operador não suportado")

        return DatasetContext(filtered)
