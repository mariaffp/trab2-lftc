def ler_automato(caminho):
    estados = []
    alfabeto = []
    inicial = ""
    finais = []
    transicoes = {}  # (estado, simbolo) -> estado de destino

    with open(caminho, encoding="utf-8") as f:
        for n, linha in enumerate(f, 1):
            linha = linha.strip()
            if linha == "":
                continue

            # as 4 primeiras linhas do arquivo são o cabeçalho
            if linha.startswith("estados:"):
                estados = linha.split(":", 1)[1].split()
            elif linha.startswith("alfabeto:"):
                alfabeto = linha.split(":", 1)[1].split()
            elif linha.startswith("inicial:"):
                inicial = linha.split(":", 1)[1].strip()
            elif linha.startswith("finais:"):
                finais = linha.split(":", 1)[1].split()
            else:
                # o resto são transições: origem simbolo destino
                partes = linha.split()
                if len(partes) != 3:
                    raise ValueError(f"linha {n}: use 'origem simbolo destino'")
                origem, simbolo, destino = partes
                if (origem, simbolo) in transicoes:
                    raise ValueError(f"linha {n}: transição repetida (AFND ainda não é suportado)")
                transicoes[(origem, simbolo)] = destino

    # a partir daqui só validação
    if len(estados) == 0 or len(alfabeto) == 0 or inicial == "":
        raise ValueError("faltou estados, alfabeto ou inicial no arquivo")
    if inicial not in estados:
        raise ValueError(f"o estado inicial {inicial} não está na lista de estados")
    for e in finais:
        if e not in estados:
            raise ValueError(f"o estado final {e} não está na lista de estados")

    for chave in transicoes:
        origem, simbolo = chave
        destino = transicoes[chave]
        if origem not in estados or destino not in estados:
            raise ValueError(f"transição com estado desconhecido: {origem} {simbolo} {destino}")
        if simbolo not in alfabeto:
            raise ValueError(f"símbolo {simbolo} não está no alfabeto")

    # AFD completo: todo estado precisa ter transição para todo símbolo
    for e in estados:
        for s in alfabeto:
            if (e, s) not in transicoes:
                raise ValueError(f"falta a transição de {e} com {s} (o AFD precisa ser completo)")

    return estados, alfabeto, inicial, finais, transicoes


def imprimir_automato(estados, alfabeto, inicial, finais, transicoes):
    # imprime no mesmo formato do arquivo de entrada
    print("estados:", " ".join(estados))
    print("alfabeto:", " ".join(alfabeto))
    print("inicial:", inicial)
    print("finais:", " ".join(finais))
    for e in estados:
        for s in alfabeto:
            print(e, s, transicoes[(e, s)])