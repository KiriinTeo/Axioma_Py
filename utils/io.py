import json, os

def salvar_dados(dados, pasta, nome_arquivo):
    extensao = ".json"
    nome_completo = nome_arquivo + extensao
    caminho = os.path.join(pasta, nome_completo)

    try:
        with open(caminho, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        print(f"Dados salvos no arquivo {nome_completo}")
    except Exception as e:
        print(f"Erro ao salvar: {e}")
