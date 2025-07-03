def calcular_desempenho(df):
    if 'horas_trabalhadas' not in df.columns or 'horas_meta' not in df.columns:
        print("As colunas 'horas_trabalhadas' e 'horas_meta' são necessárias para esta análise.")
        return None

    df['Desempenho'] = df.apply(lambda row: (
        'Abaixo da Meta' if row['horas_trabalhadas'] < 0.8 * row['horas_meta'] else
        'Dentro da Meta' if row['horas_trabalhadas'] <= 1.1 * row['horas_meta'] else
        'Acima da Meta'
    ), axis=1)

    return df
