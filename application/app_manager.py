from application.services.dataset_service import DatasetService
from application.services.plot_service import PlotService
from application.services.export_service import ExportService
from application.services.filter_service import FilterService
from application.services.analysis_service import AnalysisService

from application.use_cases.load_dataset_use_case import LoadDatasetUseCase
from application.use_cases.generate_plot_use_case import GeneratePlotUseCase
from application.use_cases.export_dataset_use_case import ExportDatasetUseCase
from application.use_cases.apply_filter_use_case import ApplyFilterUseCase
from application.use_cases.list_columns_use_case import ListColumnsUseCase
from application.use_cases.data_summary_use_case import DatasetSummaryUseCase
from application.use_cases.basic_analysis_use_case import BasicAnalysisUseCase
from application.use_cases.login_user_use_case import LoginUserUseCase
from application.use_cases.register_user_use_case import RegisterUserUseCase

class ApplicationManager:
    def __init__(self):
        # Services
        self.dataset_service = DatasetService()
        self.plot_service = PlotService()
        self.export_service = ExportService()
        self.filter_service = FilterService()
        self.analysis_service = AnalysisService()

        # Use cases (casos de uso)
        self.load_dataset_uc = LoadDatasetUseCase(self.dataset_service)
        self.generate_plot_uc = GeneratePlotUseCase(self.plot_service)
        self.export_dataset_uc = ExportDatasetUseCase(self.export_service)
        self.apply_filter_uc = ApplyFilterUseCase(self.filter_service)
        self.list_columns_uc = ListColumnsUseCase(self.dataset_service)
        self.dataset_summary_uc = DatasetSummaryUseCase(self.dataset_service)
        self.basic_analysis_uc = BasicAnalysisUseCase(self.analysis_service)
        self.login_user_uc = LoginUserUseCase()
        self.register_user_uc = RegisterUserUseCase()

manager = ApplicationManager()