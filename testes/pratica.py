def numeroDePares(a, b):
    qtde = 0
    a = [10, 4, 4, 9, 1, 0, 2, 2, 8, 5, 3, 9, 4, 6, 7]
    b = [9, 3, 3, 7, 0, 0, 9, 2, 10, 8, 2, 1, 5, 4, 6]
    used_a = set()
    used_b = set()
    pairs = []

    for i in range(len(a)):
        if a[i] > b[i] and a[i] not in used_a and b[i] not in used_b:
            pairs.append((a[i], b[i]))
            used_a.add(a[i])
            used_b.add(b[i])
            qtde += 1

    print(f"Quantidade de pares: ", qtde)
    return qtde, pairs

def manipulaFrase():
    frase = "é muito poggers novinha o python"
    palavras = frase.split()
    print(f"Número de palavras:", len(palavras))

    mais_longa = max(palavras, key=len)
    mais_curta = min(palavras, key=len)

    print(f"Palavra mais longa:", mais_longa)
    print(f"Palavra mais curta:", mais_curta)

    frase_invertida = ' '.join(reversed(palavras))
    print(f"Frase invertida:", frase_invertida)

    frequencia = {}
    for letra in frase.lower():
        if letra.isalpha():  
            frequencia[letra] = frequencia.get(letra, 0) + 1

    letra_mais_frequente = max(frequencia, key=frequencia.get)
    print(f"Letra mais frequente:", letra_mais_frequente)

    vogais = "aeiouAEIOU"
    frase_sem_vogais = ''.join([letra for letra in frase if letra not in vogais])
    print(f"Frase sem vogais:", frase_sem_vogais)

if __name__ == "__main__":
    print(numeroDePares([1, 0, 2, 2, 8, 5], [9, 3, 3, 7, 0, 0]))
    print(manipulaFrase())


