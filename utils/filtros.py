def filtrar_dados(dados, filtros):
    resultado = []
    for item in dados:
        if isinstance(item, dict):
            if all(str(item.get(campo, '')).lower() == str(valor).lower() for campo, valor in filtros.items() if valor):
                resultado.append(item)
    return resultado
