import os
import sys

# forçar o caminho pois não tava encontrando o "application"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application.services.dataset_service import DatasetService
from application.services.plot_service import PlotService
from application.use_cases.generate_plot_use_case import GeneratePlotUseCase

dataset_service = DatasetService()
plot_service = PlotService()

ctx = dataset_service.load("data/exemplo.csv") # alterar para dados quaisquer

use_case = GeneratePlotUseCase(plot_service)

fig, ax = use_case.execute(
    ctx=ctx,
    plot_type="line",
    x="coluna_x",
    y="coluna_y"
)

fig.show()
