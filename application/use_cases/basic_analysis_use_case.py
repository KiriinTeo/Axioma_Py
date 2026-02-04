class BasicAnalysisUseCase:
    def __init__(self, analysis_service):
        self.analysis_service = analysis_service

    def execute(self, ctx):
        stats = self.analysis_service.basic_stats(ctx)

        serializable = {}
        for k, v in stats.items():
            value = None
            if hasattr(v, "to_dict"):
                try:
                    value = v.to_dict()
                except Exception:
                    value = str(v)
            elif hasattr(v, "tolist"):
                try:
                    value = v.tolist()
                except Exception:
                    value = str(v)
            else:
                value = v

            # manter com certeza que as chaves do dict são strings )(pq o json obriga)
            if isinstance(value, dict):
                newd = {}
                for kk, vv in value.items():
                    newd[str(kk)] = vv
                serializable[k] = newd
            else:
                serializable[k] = value

        return serializable
