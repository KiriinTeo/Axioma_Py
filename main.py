import logging
import argparse

from analise.dadosAPI import carregarAPI
from analise.dadosFormatar import formatar_colunas
from coleta.local_Coleta import carregarArquivoLoc
from testes.exDesempenho import calcular_desempenho
from utils.carregarConfig import carregar_config
from utils.carregarData import carregarSalvos
from utils.io import salvar_dados
from utils.exibicao import exibir_dados
from visualizacao.dadosGraficos import VisualizadorDados

def parse_args():
    parser = argparse.ArgumentParser(description="Sistema Axioma_Py")
    parser.add_argument("--api_url", type=str, help="URL da API", default=None)
    parser.add_argument("--query", type=str, help="Termo de busca (padrão)", default=None)
    parser.add_argument("--limit", type=int, help="Número de resultados", default=None)
    return parser.parse_args()

def menu_principal():
    print("\n--- Sistema Axioma_Py ---")
    print("1 - Consultar dados via API")
    print("2 - Carregar dados de arquivo local")
    print("3 - Analisar dados (comparações e estatísticas)")
    print("0 - Sair")
    return input("Escolha uma opção: ")

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
            salvar_dados(dados, 'data', nome_arquivo)
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_analise(df_analise):
    while True:
        print("\n--- Menu de Análise ---")
        print("1 - Estatísticas Descritivas")
        print("2 - Histograma (Ideal para visualizar a distribuição de uma variável numérica)")
        print("3 - Gráfico de Barras (Ideal para comparar categorias)")
        print("4 - Dispersão (Ideal para analisar correlações entre variáveis numéricas)")
        print("5 - Análise de Desempenho (exemplo prático)")
        print("6 - Gráfico de Linha (Ideal para visualizar tendências ao longo do tempo)")
        print("7 - Gráfico de Pizza (Ideal para visualizar proporções de categorias)")
        print("8 - Boxplot (Ideal para visualizar a distribuição e outliers de uma variável numérica)")
        print("9 - Operações com Dados (Salvar/Visualizar)")
        print("0 - Voltar")
        opc = input("Escolha uma opção: ").strip()

        if opc == '1':
            VisualizadorDados.estatisticas_descritivas(df_analise)

        elif opc == '2':
            print("\nDica: O histograma é ideal para variáveis como preços, idades, salários, etc.")
            col = input("Informe uma coluna numérica para histograma: ").strip()
            VisualizadorDados.plot_histograma(df_analise, col)

        elif opc == '3':
            print("\nDica: O gráfico de barras é ótimo para comparar categorias como produtos, setores, cidades, etc.")
            col = input("Informe uma coluna categórica para barras: ").strip()
            topn = int(input("Top N categorias (padrão 10): ").strip() or 10)
            VisualizadorDados.plot_barras(df_analise, col, top_n=topn)

        elif opc == '4':
            print("\nDica: O gráfico de dispersão é excelente para analisar correlações, como altura vs peso, vendas vs lucro, etc.")
            print("\nDeseja ")
            x = input("Informe a coluna X (numérica) (ex: Altura, Vendas): ").strip()
            y = input("Informe a coluna Y (numérica) (ex: Peso, Lucro): ").strip()
            VisualizadorDados.plot_scatter(df_analise, x, y)

        elif opc == '5':
            df_desempenho = calcular_desempenho(df_analise)
            if df_desempenho is not None:
                print("\n--- Resultado da Análise de Desempenho ---")
                print(df_desempenho[['funcionario', 'horas_trabalhadas', 'horas_meta', 'Desempenho']])
                VisualizadorDados.plot_barras(df_desempenho, 'Desempenho')

        elif opc == '6':
            print("\nDica: O gráfico de linha (ou área) é ideal para acompanhar tendências ao longo do tempo. Ex: Data x Vendas.")
            x = input("Informe a coluna X (ex: Data, Tempo, Período): ").strip()
            y_cols = input("Informe a(s) coluna(s) Y (numérica), separadas por vírgula se mais de uma (ex: Preços, Quantidades): ").strip().split(',')
            y_cols = [col.strip() for col in y_cols if col.strip()]
            area = len(y_cols) > 1
            if area:
                VisualizadorDados.plot_linha(df_analise, x, y_cols, area=True)
            else:
                VisualizadorDados.plot_linha(df_analise, x, y_cols[0], area=False)

        elif opc == '7':
            print("\nDica: O gráfico de pizza é bom para visualizar proporções de categorias como tipos de produtos, regiões, etc.")
            col = input("Informe uma coluna categórica para o gráfico de pizza: ").strip()
            VisualizadorDados.plot_pizza(df_analise, col)

        elif opc == '8':
            print("\nDica: O boxplot é útil para visualizar a dispersão, mediana e possíveis outliers. Ex: Salário, Idade, Preço.")
            col = input("Informe uma coluna numérica para o boxplot: ").strip()
            VisualizadorDados.plot_boxplot(df_analise, col)

        elif opc == '9':
            menu_operacoes_dados(df_analise.to_dict(orient='records'))

        elif opc == '0':
            break

        else:
            print("Opção inválida.")


def fonteAnalise():
    usar_salvos = input("Usar conjunto de dados salvo em 'data/'? (s/n): ").strip().lower()
    if usar_salvos == 's':
        return carregarSalvos()

    fonte = input("1) API\n2) Arquivo local\nEscolha a fonte dos dados: ").strip()

    if fonte == '1':
        return carregarAPI()

    elif fonte == '2':
        df_local = carregarArquivoLoc()
        if df_local is not None:
            return formatar_colunas(df_local)

    print("Opção inválida ou erro ao carregar os dados.")
    return None

def main():
    config = carregar_config()
    args = parse_args()

    logging.basicConfig(level=getattr(logging, config['logging_level']))

    while True:
        opcao = menu_principal()
        match opcao:

            case '1':
                df_formatado = carregarAPI()
                if df_formatado is None:
                    print("Erro ao carregar dados da API.")
                    continue
                
                menu_operacoes_dados(df_formatado.to_dict(orient='records'))

            case '2':
                df = carregarArquivoLoc()
                if df is not None:
                    df_formatado = formatar_colunas(df)
                    if df_formatado is not None:
                        menu_operacoes_dados(df_formatado.to_dict(orient='records'))

            case '3':
                print("\n--- Análise de Dados ---")
                df_analise = fonteAnalise()
                if df_analise is not None:
                    menu_analise(df_analise)

            case '0':
                print("\nEncerrando o sistema. Obrigado por utilizar o Axioma_Py.")
                break

            case _:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
