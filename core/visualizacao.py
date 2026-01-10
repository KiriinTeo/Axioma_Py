from typing import Dict, Any, Optional
import matplotlib
matplotlib.use("Agg")  # Usar backend sem interface gráfica

import matplotlib.pyplot as plt
from core.contexto import DatasetContext

def generate_plot(
    ctx: DatasetContext,
    plot_type: str,
    x: Optional[str] = None,
    y: Optional[str] = None,
    title: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    user: Optional[str] = None
):
    if options is None:
        # onde fica as opções alteração dos gráficos disponiveis 
        # informação puxada do usuário ou da requisição específica, não generalizar toda instância aqui ou o código morre :v 
        options = { } 

    df = ctx.dataframe

    fig, ax = plt.subplots()

    match plot_type:
        case "line":
            if not x or not y:
                raise ValueError("line exige x e y")
            ax.plot(df[x], df[y], **options)

        case "bar":
            if not x or not y:
                raise ValueError("bar exige x e y")
            ax.bar(df[x], df[y], **options)

        case "scatter":
            if not x or not y:
                raise ValueError("scatter exige x e y")
            ax.scatter(df[x], df[y], **options)

        case "hist":
            if not x:
                raise ValueError("histograma exige x")
            ax.hist(df[x], **options)

        case "box":
            if not x:
                raise ValueError("boxplot exige x")
            ax.boxplot(df[x], **options)

        case "area":
            if not x or not y:
                raise ValueError("area exige x e y")
            x_ordenado = df[x].sort_values()
            ax.fill_between(x_ordenado, df.loc[x_ordenado.index, y], **options)

        case "heatmap":
            if not x or not y:
                raise ValueError("heatmap exige x e y")
            corr = df.corr()
            ax.imshow(corr, **options)
            ax.set_xticks(range(len(corr.columns)))
            ax.set_yticks(range(len(corr.columns)))
            ax.set_xticklabels(corr.columns)
            ax.set_yticklabels(corr.columns)

        case "violin":
            if not x:
                raise ValueError("violin exige x")
            ax.violinplot(df[x], **options)

        # case "stack_bar": / Fazer uma função só pra ele se necessário

        case _:
            raise ValueError(f"Tipo de gráfico não suportado: {plot_type}")

    ax.set_title(title or ctx.name)
    ax.set_xlabel(x or "")
    ax.set_ylabel(y or "")

    return fig
