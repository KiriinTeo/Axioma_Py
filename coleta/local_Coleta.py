import pandas as pd
from utils.selectArquivo import selecionar_arquivo

def carregarArquivoLoc():
    caminho = selecionar_arquivo()
    if not caminho:
        print("Nenhum arquivo foi selecionado.")
        return None

    try:
        if caminho.endswith('.csv'):
            df = pd.read_csv(caminho)
        elif caminho.endswith('.json'):
            df = pd.read_json(caminho)
        else:
            print("Formato de arquivo não suportado.")
            return None

        print("Arquivo carregado com sucesso.")
        return df

    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return None
