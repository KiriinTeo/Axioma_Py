import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

class VisualizadorDados:
    @staticmethod
    def estatisticas_descritivas(df: pd.DataFrame):
        print("\n--- Estatísticas Descritivas ---")
        print(df.describe(include='all'))

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
