import requests
from utils.normalizacao import normalizar_json

class APIDados:
    def __init__(self, config):
        self.base_url = config["url"]
        self.params_keys = config.get("params", [])
        self.response_path = config.get("default_response_path", "")
        self.default_fields = config.get("default_fields", [])
        self.api_key_required = config.get("requires_key", False)

        self.params = {}

    # def solicitar_parametros(self):
        # for param in self.params_keys:
            # valor = input(f"Digite o valor para '{param}': ")
            # self.params[param] = valor

    def consultar(self):
        try:
            response = requests.get(self.base_url, params=self.params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Erro ao acessar a API: {e}")
            return None

    def consultar_dataframe(self):
        dados_json = self.consultar()
        if not dados_json:
            return None

        df = normalizar_json(dados_json, chave_raiz=self.response_path)

        if df is not None and not df.empty:
            print("\nDados coletados da API com sucesso!")
            return df
        else:
            print("Nenhum dado encontrado na API.")
            return None


