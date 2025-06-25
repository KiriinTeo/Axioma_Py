import json

def salvar_dados(dados, nome_arquivo):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        print(f"Dados salvos no arquivo {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar: {e}")
