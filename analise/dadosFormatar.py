def formatar_colunas(df, colunas_selecionadas=None):
    print(f"\nColunas disponíveis no arquivo: {list(df.columns)}")

    df.columns = df.columns.str.strip()

    if colunas_selecionadas is None:
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
            return df_formatado
        except Exception as e:
            print(f"Erro ao formatar os dados: {e}")
            return None

    else:
        colunas_selecionadas = [col.strip() for col in colunas_selecionadas]
        try:
            df_formatado = df[colunas_selecionadas].copy()
            df_formatado.columns = [col.strip() for col in df_formatado.columns]
            print("\nDados formatados com sucesso!")
            return df_formatado
        
        except Exception as e:
            print(f"Erro ao formatar os dados: {e}")
            return None
