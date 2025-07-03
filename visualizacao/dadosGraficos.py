import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

class VisualizadorDados:
    @staticmethod
    def estatisticas_descritivas(df: pd.DataFrame):
        print("\n--- Estatísticas Descritivas ---")
        descricao = df.describe(include='all').round(2)

        plt.figure(figsize=(12, 4))
        tabela = plt.table(cellText=descricao.values,
              colLabels=descricao.columns,
              rowLabels=descricao.index,
              loc='center',
              )
        tabela.set_fontsize(20)
        plt.axis('off')
        plt.title('Estatísticas Descritivas')
        plt.show()

    @staticmethod
    def plot_histograma(df: pd.DataFrame, coluna: str):
        if coluna not in df.columns:
            print(f"Coluna '{coluna}' não encontrada.")
            return
        plt.figure()
        sns.histplot(df[coluna].dropna(), kde=True)
        plt.title(f"Histograma de {coluna}")
        plt.xlabel(coluna)
        plt.ylabel("Frequência")
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
        plt.show()

    @staticmethod
    def plot_barras(df: pd.DataFrame, coluna: str, top_n: int = 10):
        if coluna not in df.columns:
            print(f"Coluna '{coluna}' não encontrada.")
            return
        contagens = df[coluna].value_counts().nlargest(top_n)
        plt.figure()
        sns.barplot(x=contagens.values, y=contagens.index)
        plt.title(f"Top {top_n} categorias em {coluna}")
        plt.xlabel("Contagem")
        plt.ylabel(coluna)
        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
        plt.show()

    @staticmethod
    def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str):
        if x_col not in df.columns or y_col not in df.columns:
            print(f"Colunas '{x_col}' ou '{y_col}' não encontradas.")
            return
        plt.figure()
        sns.scatterplot(data=df, x=x_col, y=y_col)
        plt.title(f"Dispersão: {x_col} vs {y_col}")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.show()

    @staticmethod
    def plot_pizza(df: pd.DataFrame, coluna: str):
        if coluna not in df.columns:
            print(f"Coluna '{coluna}' não encontrada.")
            return
        contagens = df[coluna].value_counts()
        plt.figure()
        plt.pie(contagens.values, labels=contagens.index, autopct='%1.1f%%', startangle=140)
        plt.title(f"Distribuição percentual de {coluna}")
        plt.show()

    @staticmethod
    def plot_boxplot(df: pd.DataFrame, coluna: str):
        if coluna not in df.columns:
            print(f"Coluna '{coluna}' não encontrada.")
            return
        plt.figure()
        sns.boxplot(y=df[coluna].dropna())
        plt.title(f"Boxplot de {coluna}")
        plt.ylabel(coluna)
        plt.show()

    @staticmethod
    def plot_linha(df: pd.DataFrame, x_col: str, y_col: str):
        if x_col not in df.columns or y_col not in df.columns:
            print(f"Colunas '{x_col}' ou '{y_col}' não encontradas.")
            return
        plt.figure()
        sns.lineplot(data=df, x=x_col, y=y_col, marker="o")
        plt.title(f"Tendência: {y_col} ao longo de {x_col}")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.show()
