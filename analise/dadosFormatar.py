def padronizar_dados(df, mapeamento_usuario):
    """
    df: DataFrame carregado
    mapeamento_usuario: dict onde o usuário informa qual coluna representa cada campo padrão.
    Exemplo:
        {
            'title': 'Nome do Livro',
            'author': 'Escritor',
            'year': 'Ano de Publicação',
            'location': 'País de Origem'
        }
    """

    try:
        df_padrao = {}

        df_padrao = df.rename(columns=mapeamento_usuario)

        campos_padroes = list(mapeamento_usuario.keys())
        for campo in campos_padroes:
            if campo not in df_padrao.columns:
                df_padrao[campo] = 'N/A'

        # Opcional: garantir que campos como autor e isbn sejam listas
        if 'author' in df_padrao.columns:
            df_padrao['author'] = df_padrao['author'].apply(lambda x: x if isinstance(x, list) else [x])

        if 'isbn' in df_padrao.columns:
            df_padrao['isbn'] = df_padrao['isbn'].apply(lambda x: x if isinstance(x, list) else [x])

        return df_padrao.to_dict(orient='records')

    except Exception as e:
        print(f"Erro ao padronizar os dados: {e}")
        return None
