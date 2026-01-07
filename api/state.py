from core.contexto import DatasetContext

# cache em memória
contexts: dict[tuple[int, str], DatasetContext] = {}
