def renomear_colunas(colunas_selecionadas):
    novo_mapeamento = {}

    for coluna in colunas_selecionadas:
        novo_nome = input(f"Digite o novo nome para a coluna '{coluna}' (ou pressione Enter para manter o nome atual): ").strip()
        if novo_nome:
            novo_mapeamento[coluna] = novo_nome
        else:
            novo_mapeamento[coluna] = coluna 

    return novo_mapeamento
