import json

def carregar_configuracoes_api():
    with open('api_Config.json', 'r', encoding='utf-8') as file:
        return json.load(file)
    
def retornar_nomesAPI():
    with open('api_Config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
        config.keys()
        return list(config.keys())
