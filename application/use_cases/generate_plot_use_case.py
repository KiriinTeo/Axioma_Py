class GeneratePlotUseCase:
    def __init__(self, plot_service):
        self.plot_service = plot_service

    def execute(self, ctx, plot_type, x=None, y=None, title=None, options=None):
        return self.plot_service.generate(
            ctx=ctx,
            plot_type=plot_type,
            x=x,
            y=y,
            title=title,
            options=options
        )
