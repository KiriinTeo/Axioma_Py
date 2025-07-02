import os
import pandas as pd

def listarArquivos(extensao='.json'):
    pasta = 'data'
    try:
        arquivos = [f for f in os.listdir(pasta) if f.endswith(extensao)]
        return arquivos
    except FileNotFoundError:
        print("Pasta 'data' não encontrada.")
        return []

def carregarSalvos():
    arquivos = listarArquivos('.json')
    if not arquivos:
        print("Nenhum arquivo JSON encontrado em 'data/'.")
        return None

    print("\nArquivos disponíveis em 'data/':")
    for i, nome in enumerate(arquivos, 1):
        print(f"{i}. {nome}")

    escolha = input("Escolha o número do arquivo a carregar (ou Enter para cancelar): ").strip()
    if not escolha.isdigit() or not (1 <= int(escolha) <= len(arquivos)):
        print("Operação cancelada ou escolha inválida.")
        return None

    caminho = os.path.join('data', arquivos[int(escolha) - 1])
    try:
        df = pd.read_json(caminho)
        print(f"Arquivo '{arquivos[int(escolha)-1]}' carregado com sucesso.")
        return df
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None
