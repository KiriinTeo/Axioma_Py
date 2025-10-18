import pandas as pd
from utils.selectArquivo import selecionar_arquivo

def carregarArquivoLoc(caminho):
    if not caminho:
        print("Nenhum arquivo foi selecionado.")
        return None

    try:
        if caminho.endswith('.csv'):
            try:
                df = pd.read_csv(caminho)
                df.columns = df.columns.str.strip()

            except UnicodeDecodeError:
                print("Arquivo com codificação diferente de UTF-8. Tentando com 'latin1'...")
                df = pd.read_csv(caminho, encoding='latin1')
                df.columns = df.columns.str.strip()

        elif caminho.endswith('.json'):
            try:
                df = pd.read_json(caminho)
            except UnicodeDecodeError:
                print("Arquivo com codificação diferente de UTF-8. Tentando com 'latin1'...")
                df = pd.read_json(caminho, encoding='latin1')

        else:
            print("Formato de arquivo não suportado.")
            return None

        print("Arquivo carregado com sucesso.")
        return df

    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return None
