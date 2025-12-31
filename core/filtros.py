from typing import Any, List
from core.contexto import DatasetContext

# sessão para filtragem simples do DF
def filter_equals(ctx: DatasetContext, column: str, value: Any):
    df = ctx.dataframe
    return ctx.__class__(
        name=ctx.name,
        dataframe=df[df[column] == value],
        metadata=ctx.metadata
    )


def filter_in(ctx: DatasetContext, column: str, values: List[Any]):
    df = ctx.dataframe
    return ctx.__class__(
        name=ctx.name,
        dataframe=df[df[column].isin(values)],
        metadata=ctx.metadata
    )
