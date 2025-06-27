from utils.carregarConfig import carregar_config
from analise.dadosAPI import LivrosAPI
from analise.dadosFormatar import formatar_colunas
from coleta.local_Coleta import carregarArquivoLoc
from utils.io import salvar_dados
from utils.exibicao import exibir_dados

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
    print("3 - Realizar scraping (a implementar)")
    print("4 - Analisar dados (visualização e estatísticas)")
    print("5 - Rodar testes de desenvolvimento")
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
                isbn = input("Digite o ISBN para busca específica (ou deixe vazio para buscar por autor/título): ")

                if isbn.strip() == '':
                    api_url = args.api_url if args.api_url else config['api_url']
                    query = args.query if args.query else input(f"Digite o termo de busca (padrão: {config['default_query']}): ") or config['default_query']
                    limit = args.limit if args.limit else config['default_limit']

                    logging.info(f"Buscando '{query}' na API: {api_url} com limite {limit}")
                    api = LivrosAPI(api_url=api_url, query=query, limit=limit)
                else:
                    api_url = "https://openlibrary.org/api/books"
                    logging.info(f"Buscando ISBN '{isbn}' na API: {api_url}")
                    api = LivrosAPI(api_url=api_url, isbn=isbn)

                dados = api.tratar_resposta()

                if not dados:
                    print("Nenhum dado encontrado.")
                    continue

                menu_operacoes_dados(dados)

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
