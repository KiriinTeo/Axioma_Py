def test_generate_plot_returns_figure():
    from application.use_cases.generate_plot_use_case import GeneratePlotUseCase
    from application.services.plot_service import PlotService
    from core.contexto import DatasetContext
    import pandas as pd

    df = pd.DataFrame({
        "x": [1, 2, 3],
        "y": [4, 5, 6]
    })

    ctx = DatasetContext(df)
    use_case = GeneratePlotUseCase(PlotService())

    fig, ax = use_case.execute(
        ctx=ctx,
        plot_type="line",
        x="x",
        y="y"
    )

    assert fig is not None
    assert ax is not None
