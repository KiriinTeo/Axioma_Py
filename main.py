from utils.carregarConfig import carregar_config
from coleta.api_Coleta import APIDados
from analise.dadosFormatar import formatar_colunas
from coleta.local_Coleta import carregarArquivoLoc
from utils.io import salvar_dados
from utils.exibicao import exibir_dados
from utils.leitorAPIconfig import carregar_configuracoes_api, retornar_nomesAPI
from utils.renomeador import renomear_colunas

import logging
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Sistema Axioma_Py")
    parser.add_argument("--isbn", type=str, help="ISBN para busca específica", default=None)
    parser.add_argument("--api_url", type=str, help="URL da API", default=None)
    parser.add_argument("--query", type=str, help="Termo de busca (padrão)", default=None)
    parser.add_argument("--limit", type=int, help="Número de resultados", default=None)
    return parser.parse_args()

def menu_principal():
    print("\n--- Sistema Axioma_Py ---")
    print("1 - Consultar dados via API")
    print("2 - Carregar dados de arquivo local")
    print("3 - Realizar scraping (em desenvolvimento)")
    print("4 - Analisar dados (comparações e estatísticas)")
    print("5 - Teste Gerais (em desenvolvimento)")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")
    return opcao

def menu_operacoes_dados(dados):
    while True:
        print("\n--- Operações com Dados ---")
        print("1 - Visualizar dados no terminal")
        print("2 - Salvar dados no arquivo JSON")
        print("0 - Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            exibir_dados(dados)

        elif opcao == '2':
            nome_arquivo = input("Digite o nome do arquivo para salvar: ")
            pasta_dados = 'data'
            salvar_dados(dados, pasta_dados, nome_arquivo)

        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")

def main():
    config = carregar_config()
    args = parse_args()

    logging.basicConfig(level=getattr(logging, config['logging_level']))

    while True:
        opcao = menu_principal()
        match opcao:
           
            case '1':      
                disponiveis_api = carregar_configuracoes_api()
                listaAPI = retornar_nomesAPI()

                print(f"Api`s Disponiveis: {listaAPI}")
                nome_api = input("Digite o nome da API (ex: openlibrary, freetogame): ").strip().lower()

                if nome_api not in disponiveis_api:
                    print("API não configurada.")
                    continue

                api_config = disponiveis_api[nome_api]
                api = APIDados(api_config)
                api.solicitar_parametros()

                df = api.consultar_dataframe()
                if df is None:
                    continue

                print("\nColunas disponíveis no arquivo:")
                print(df.columns.tolist())

                colunas_selecionadas = input("Digite as colunas que deseja manter, separadas por vírgula: ").split(',')
                colunas_selecionadas = [col.strip() for col in colunas_selecionadas]

                try:
                    df_formatado = df[colunas_selecionadas]

                    novo_mapeamento = renomear_colunas(colunas_selecionadas)
                    df_formatado = df_formatado.rename(columns=novo_mapeamento)

                    print("\nDados formatados com sucesso!")

                except Exception as e:
                    print(f"Erro ao formatar os dados: {e}")
                    continue

                menu_operacoes_dados(df_formatado.to_dict(orient='records'))

            case '2':  
                print("\n--- Carregar Arquivo Local ---")
                df = carregarArquivoLoc()
                if df is not None:
                    dados_formatados = formatar_colunas(df)
                    if dados_formatados:
                        menu_operacoes_dados(dados_formatados)
                    else:
                        print("Falha ao formatar os dados.")

            case '3':
                print("\n--- Coleta via Scraping (a ser implementado) ---")

            case '4':
                print("\n--- Análise de Dados ---")
                # an álise de gráficos e estatísticas

            case '5':
                print("\n--- Ambiente de Testes ---")

            case '0':
                print("\nEncerrando o sistema. Obrigado por utilizar o Axioma_Py.")
                break

            case _:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
