"""
Script para criar as tabelas no Oracle
Execute antes de rodar a aplicação
"""

from infra.database.connection import engine
from infra.database.base import Base
from infra.database.models.user import UserModel
from infra.database.models.dataset import DatasetModel
from infra.database.models.filter import FilterModel
from infra.database.models.plot import PlotModel
from infra.database.models.export import ExportModel
from infra.database.models.analysis import AnalysisModel

print("Criando tabelas no Oracle...")

try:
    Base.metadata.create_all(bind=engine)
    print("✓ Tabelas criadas com sucesso!")
    print("\nTabelas criadas:")
    print("  ✓ users")
    print("  ✓ datasets")
    print("  ✓ filters")
    print("  ✓ plots")
    print("  ✓ exports")
    print("  ✓ analyses")
except Exception as e:
    print(f"✗ Erro ao criar tabelas: {e}")
    import traceback
    traceback.print_exc()
