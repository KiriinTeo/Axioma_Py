from typing import Dict, Any
from core.contexto import DatasetContext

def describe(ctx: DatasetContext) -> Dict[str, Any]:
    return ctx.dataframe.describe(include="all").to_dict()
    # pra estatisticas básicas

def null_summary(ctx: DatasetContext) -> Dict[str, int]:
    return ctx.dataframe.isnull().sum().to_dict()
    # pra sumário de nulos

