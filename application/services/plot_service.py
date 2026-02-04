from core.visualizacao import generate_plot

class PlotService:
    def generate(self, **kwargs):
        return generate_plot(**kwargs)
