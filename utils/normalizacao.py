import pandas as pd

def normalizar_json(dados_json, chave_raiz=None):
    try:
        if chave_raiz:
            for chave in chave_raiz.split('.'):
                dados_json = dados_json.get(chave, [])

        if isinstance(dados_json, list):
            df = pd.json_normalize(dados_json)
        elif isinstance(dados_json, dict):
            if all(isinstance(v, dict) for v in dados_json.values()):
                df = pd.json_normalize(list(dados_json.values()))
            else:
                df = pd.json_normalize(dados_json)
        else:
            raise Exception("Formato de dados não reconhecido para normalização.")

        return df

    except Exception as e:
        print(f"Erro ao normalizar os dados: {e}")
        return None
