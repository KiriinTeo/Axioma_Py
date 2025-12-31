import pandas as pd
from utils.selectArquivo import selecionar_arquivo

def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def load_json(path: str) -> pd.DataFrame:
    return pd.read_json(path)
