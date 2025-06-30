import matplotlib.pyplot as plt
from analise.analiseLivros import formatacaoDados, pesquisarLivro, pd

df = formatacaoDados(pesquisarLivro(titulo="The Hobbit", autor="J.R.R. Tolkien"))

dados_opcoes = {
    "1": {
        "titulo": "Livros por Ano de Publicação",
        "dados": df["Ano de Publicação"].value_counts().sort_index(),
        "xlabel": "Ano de Publicação",
        "ylabel": "Quantidade de Livros",
        "tipo_sugerido": ["bar", "line", "scatter"]
    },
    "2": {
        "titulo": "Livros por Autores",
        "dados": df["Autor"].value_counts().head(10),
        "xlabel": "Autor",
        "ylabel": "Quantidade de Livros",
        "tipo_sugerido": ["bar", "pie"]
    },
    "3": {
        "titulo": "Livros por Editora",
        "dados": df["Editora"].value_counts().head(5),
        "xlabel": "Editora",
        "ylabel": "Quantidade de Livros",
        "tipo_sugerido": ["bar", "pie"]
    }
}

graficos_opcoes = {
    "1": "bar",
    "2": "line",
    "3": "pie",
    "4": "hist",
    "5": "scatter"
}

def plotar_grafico(tipo, dados, titulo, xlabel=None, ylabel=None, **kwargs):
    plt.figure(figsize=(10, 6))
    
    if tipo == "bar":
        dados.plot(kind="bar", color=kwargs.get("color", "blue"))
    elif tipo == "line":
        dados.plot(kind="line", marker="o", color=kwargs.get("color", "red"))
    elif tipo == "pie":
        plt.figure(figsize=(8, 8))
        dados.plot(kind="pie", autopct='%1.1f%%', startangle=90, cmap=kwargs.get("cmap", "coolwarm"))
        plt.ylabel("")
    elif tipo == "hist":
        if not pd.api.types.is_numeric_dtype(dados.index):
            print("\n⚠️ Histograma exige dados numéricos. Escolha outro tipo de gráfico.\n")
            return
        dados.dropna().astype(int).hist(bins=kwargs.get("bins", 20), color=kwargs.get("color", "purple"), edgecolor="black")
    elif tipo == "scatter":
        if "Ano de Publicação" in df.columns:
            anos_publicacao = df["Ano de Publicação"].dropna().astype(int)
            contagem_por_ano = anos_publicacao.value_counts().sort_index()
            plt.scatter(contagem_por_ano.index, contagem_por_ano.values, alpha=0.5, color=kwargs.get("color", "blue"))
            xlabel, ylabel = "Ano de Publicação", "Quantidade de Livros Publicados"
        else:
            print("\n⚠️ Scatter requer duas variáveis numéricas. Escolha outro tipo de gráfico.\n")
            return

    plt.title(titulo)
    if xlabel:
        plt.xlabel(xlabel.replace("_", " "))  
    if ylabel:
        plt.ylabel(ylabel.replace("_", " ")) 

    plt.xticks(rotation=45) 
    plt.grid(True, linestyle="--", alpha=0.6) 
    plt.show()
    input("\nPressione Enter para continuar...")

def miniMenu():
    while True:
        print("\nEscolha os dados que deseja visualizar:")
        for key, value in dados_opcoes.items():
            print(f"{key} - {value['titulo']}")

        opcao_dado = input("\nDigite o número da opção (ou 'q' para sair): ")
        if opcao_dado.lower() == "q":
            break
        elif opcao_dado not in dados_opcoes:
            print("Opção inválida! Tente novamente.")
            continue

        dados_selecionados = dados_opcoes[opcao_dado]

        print("\nEscolha o tipo de gráfico:")
        for key, nome in graficos_opcoes.items():
            compatibilidade = "✅" if graficos_opcoes[key] in dados_selecionados["tipo_sugerido"] else "⚠️"
            print(f"{key} - {nome.capitalize()} {compatibilidade}")

        opcao_grafico = input("\nDigite o número do gráfico desejado: ")
        if opcao_grafico not in graficos_opcoes:
            print("Opção inválida! Tente novamente.")
            continue

        tipo_grafico = graficos_opcoes[opcao_grafico]

        if tipo_grafico not in dados_selecionados["tipo_sugerido"]:
            print(f"\n⚠️ O gráfico '{tipo_grafico}' pode não ser adequado para estes dados!\n")

        plotar_grafico(tipo_grafico, dados_selecionados["dados"], dados_selecionados["titulo"], 
                       dados_selecionados["xlabel"], dados_selecionados["ylabel"])

#Graficos criados e otimizados para direntes tipos de dados, sujeito a atualizações com futuros testes.
miniMenu()
