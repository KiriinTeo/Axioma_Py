import requests

class APIDados:
    def __init__(self, base_url, params=None):
        self.base_url = base_url
        self.params = params or {}

    def consultar(self):
        try:
            response = requests.get(self.base_url, params=self.params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Erro ao acessar a API: {e}")
