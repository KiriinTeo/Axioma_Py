def formatar_colunas(df):
    print(f"\nColunas disponíveis no arquivo: {list(df.columns)}")

    colunas_selecionadas = input("Digite as colunas que deseja manter, separadas por vírgula: ").split(',')
    colunas_selecionadas = [col.strip() for col in colunas_selecionadas]

    mapeamento = {}
    for coluna in colunas_selecionadas:
        novo_nome = input(f"Digite o novo nome para a coluna '{coluna}' (ou pressione Enter para manter o nome atual): ")
        if novo_nome.strip():
            mapeamento[coluna] = novo_nome.strip()
        else:
            mapeamento[coluna] = coluna  

    try:
        df_formatado = df[colunas_selecionadas].rename(columns=mapeamento)
        print("\nDados formatados com sucesso!")
        return df_formatado.to_dict(orient='records')
    except Exception as e:
        print(f"Erro ao formatar os dados: {e}")
        return None
