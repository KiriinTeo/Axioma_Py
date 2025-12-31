class ApplyFilterUseCase:
    def __init__(self, filter_service):
        self.filter_service = filter_service

    def execute(self, ctx, column, operator, value):
        return self.filter_service.apply(ctx, column, operator, value)
