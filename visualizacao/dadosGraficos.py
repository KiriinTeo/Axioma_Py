import pandas as pd
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

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
        tabela.set_fontsize(13)
        plt.axis('off')
        plt.title('Estatísticas Descritivas')
        plt.show()

    @staticmethod
    def plot_histograma(df: pd.DataFrame, coluna: str, tituloHist, bins='auto'):
        if coluna not in df.columns:
            print(f"Coluna '{coluna}' não encontrada.")
            return

        dados = df[coluna].dropna()
        plt.figure()
        sns.histplot(dados, bins=bins, kde=True)
        plt.title(tituloHist)
        plt.xlabel(coluna)
        plt.ylabel("Frequência")
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))
        plt.show()

    @staticmethod
    def plot_barras(df: pd.DataFrame, coluna: str, tituloBar: str, top_n: int = 10):
        if coluna not in df.columns:
            print(f"Coluna '{coluna}' não encontrada.")
            return
        
        contagens = df[coluna].value_counts().nlargest(top_n)
        plt.figure()
        sns.barplot(x=contagens.values, y=contagens.index)
        plt.title(tituloBar)
        plt.xlabel("Quantidade")
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
        sns.boxplot(y=df[coluna].dropna(), orientation='vertical')
        plt.title(f"Distribuição de {coluna}")
        plt.ylabel(coluna)
        plt.show()

    @staticmethod
    def plot_linha(df: pd.DataFrame, x_col: str, y_col: str, area=False):
        if isinstance(y_col, list):
            faltantes = [col for col in [x_col] + y_col if col not in df.columns]
        else:
            faltantes = [col for col in [x_col, y_col] if col not in df.columns]
        if faltantes:
            print(f"Colunas não encontradas: {', '.join(faltantes)}")
            return

        x = df[x_col].values

        if area:
            if not isinstance(y_col, list):
                print("Para gráfico de área, forneça uma lista de colunas para 'y_col'.")
                return
            ys = [df[col].values for col in y_col]
            fig, ax = plt.subplots()
            # stackplot espera 1D arrays, sem NaN. Substitui NaN por zero.
            ys_clean = [np.nan_to_num(y) for y in ys]
            ax.stackplot(x, *ys_clean, labels=y_col, alpha=0.8)
            ax.legend(loc='upper left')
            ax.set_title(f"Gráfico de Área: {', '.join(y_col)} ao longo de {x_col}")
            ax.set_xlabel(x_col)
            ax.set_ylabel("Valores")
            plt.tight_layout()
            plt.show()
        else:
            plt.figure()
            if isinstance(y_col, list):
                for col in y_col:
                    sns.lineplot(data=df, x=x_col, y=col, marker="o", label=col)
                plt.legend()
            else:
                sns.lineplot(data=df, x=x_col, y=y_col, marker="o")
            plt.title(f"Tendência: {y_col} ao longo de {x_col}")
            plt.xlabel(x_col)
            plt.ylabel(y_col if not isinstance(y_col, list) else "Valores")
            plt.tight_layout()
            plt.show()
