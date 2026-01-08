from typing import Dict, Tuple
from core.contexto import DatasetContext

# cache mais explícito pq o geral tava dando b.o 
contexts: Dict[Tuple[int, str], DatasetContext] = {}
