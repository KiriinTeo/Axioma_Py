class BasicAnalysisUseCase:
    def __init__(self, analysis_service):
        self.analysis_service = analysis_service

    def execute(self, ctx):
        return self.analysis_service.basic_stats(ctx).to_dict()
