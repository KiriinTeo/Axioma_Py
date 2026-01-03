import pandas as pd

from core.contexto import DatasetContext
from core.analises import describe, null_summary
from core.filtros import filter_equals, filter_in
from core.visualizacao import generate_plot
from core.pipeline import Pipeline

def create_sample_dataset():
    data = {
        "produto": ["A", "B", "C", "A", "B", "C"],
        "categoria": ["X", "X", "Y", "Y", "X", "Y"],
        "status": ["ativo", "ativo", "inativo", "ativo", "inativo", "ativo"],
        "valor": [100, 150, 200, 120, 180, 220],
        "quantidade": [10, 5, 8, 12, 6, 7]
    }
    return pd.DataFrame(data)

df = create_sample_dataset()
ctx = DatasetContext(name="Dataset de Teste", dataframe=df)

def test_context():
    print("Contexto criado:")
    print("Shape:", ctx.shape())
    print("Colunas:", ctx.columns())
    print()

def test_analytics(ctx):
    print("Estatísticas descritivas:")
    stats = describe(ctx)
    print(stats)
    print()

    print("Resumo de valores nulos:")
    nulls = null_summary(ctx)
    print(nulls)
    print()

def test_filters(ctx):
    print("Aplicando filtros...")

    ctx_ativo = filter_equals(ctx, "status", "ativo")
    print("Registros ativos:", ctx_ativo.shape())

    ctx_categoria = filter_in(ctx_ativo, "categoria", ["X"])
    print("Ativos da categoria X:", ctx_categoria.shape())

    print()
    assert ctx_categoria

def test_visualization(ctx):
    print("Gerando gráfico de barras...")

    fig = generate_plot(
        ctx=ctx,
        plot_type="scatter",
        x="produto",
        y="valor",
        title="Valor por Produto",
        options={"color": "#000000", "linestyle": ":", "linewidth": 2, "marker": "+"}
    )

    # Mostrar o gráfico SOMENTE AQUI (fora do core
    import matplotlib.pyplot as plt
    plt.show()

    print("Gráfico exibido com sucesso.")
    print()

def test_pipeline(ctx):
    print("Executando pipeline...")

    pipeline = Pipeline()
    pipeline.add_step(lambda c: filter_equals(c, "status", "ativo"))
    pipeline.add_step(lambda c: filter_in(c, "categoria", ["Y"]))

    ctx_final = pipeline.run(ctx)

    print("Resultado do pipeline:")
    print(ctx_final.dataframe)
    print()

if __name__ == "__main__":
    print("=== testes de core Axioma ===\n")

    test_context()

    base_df = create_sample_dataset()
    base_ctx = DatasetContext(name="Dataset Base", dataframe=base_df)

    test_analytics(base_ctx)

    filtered_ctx = test_filters(base_ctx)

    test_visualization(filtered_ctx)

    test_pipeline(base_ctx)

    print("=== todos testes executados ===")
