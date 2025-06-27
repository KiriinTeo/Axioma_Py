def exibir_dados(dados):
    if not dados:
        print("Nenhum dado para exibir.")
        return

    for idx, item in enumerate(dados, 1):
        print(f"--- Registro {idx} ---")
        for chave, valor in item.items():
            if isinstance(valor, list):
                valor = ', '.join(str(v) for v in valor)
            print(f"{chave}: {valor}")
        print("-" * 40)
