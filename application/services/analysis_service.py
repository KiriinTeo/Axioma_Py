class AnalysisService:
    from core.contexto import DatasetContext
    
    def basic_stats(self, ctx: DatasetContext):
        return {
            "mean": ctx.dataframe.mean(numeric_only=True),
            "median": ctx.dataframe.median(numeric_only=True),
            "std": ctx.dataframe.std(numeric_only=True),
        }
    
    # adicionar todos os dados básico analítcos aqui (frequencias, quantidade etc etc)
