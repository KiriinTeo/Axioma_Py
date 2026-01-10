class AnalysisService:
    from core.contexto import DatasetContext
    
    def basic_stats(self, ctx: DatasetContext):
        stat_info = {
            "mean": ctx.dataframe.mean(numeric_only=True),
            "median": ctx.dataframe.median(numeric_only=True),
            "std": ctx.dataframe.std(numeric_only=True),
            "min": ctx.dataframe.min(numeric_only=True),
            "max": ctx.dataframe.max(numeric_only=True),
            "count": ctx.dataframe.count(),
            "missing_values": ctx.dataframe.isnull().sum(),
            "frequency": ctx.dataframe.value_counts(),
            "unique_values": ctx.dataframe.nunique()
        }

        return stat_info
    
    # adicionar todos os dados básico analítcos aqui (frequencias, quantidade etc etc)
