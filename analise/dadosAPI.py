from utils.leitorAPIconfig import carregar_configuracoes_api, retornar_nomesAPI
from coleta.api_Coleta import APIDados
from analise.dadosFormatar import formatar_colunas

def carregarAPI(): 
    disponiveis_api = carregar_configuracoes_api()
    listaAPI = retornar_nomesAPI()

    print(f"Api`s Disponiveis: {listaAPI}")
    nome_api = input("Digite o nome da API (ex: openlibrary, freetogame): ").strip().lower()

    if nome_api not in disponiveis_api:
        print("API não configurada.")
        return

    api_config = disponiveis_api[nome_api]
    api = APIDados(api_config)
    api.solicitar_parametros()

    df = api.consultar_dataframe()
    if df is None:
        return

    try:
        df_formatado = formatar_colunas(df)
        if df_formatado is None:
            print("Falha ao formatar os dados.")
            return
        
        print("\nDados formatados com sucesso!")
        return df_formatado

    except Exception as e:
        print(f"Erro ao formatar os dados: {e}")
        return
