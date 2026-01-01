import os
import sys

# Ensure project root is on sys.path for pytest runs
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest


@pytest.fixture(scope="module")
def ctx():
    # Provide a default sample DatasetContext for tests that request `ctx`
    import pandas as pd
    from core.contexto import DatasetContext

    data = {
        "produto": ["A", "B", "C", "A", "B", "C"],
        "categoria": ["X", "X", "Y", "Y", "X", "Y"],
        "status": ["ativo", "ativo", "inativo", "ativo", "inativo", "ativo"],
        "valor": [100, 150, 200, 120, 180, 220],
        "quantidade": [10, 5, 8, 12, 6, 7]
    }

    df = pd.DataFrame(data)
    return DatasetContext(name="Dataset de Teste", dataframe=df)
