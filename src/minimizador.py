def remover_inalcancaveis(estados, alfabeto, inicial, finais, transicoes):
    # busca a partir do inicial, guardando todos os estados que dá pra chegar
    alcancaveis = [inicial]
    fila = [inicial]
    while len(fila) > 0:
        atual = fila.pop(0)
        for s in alfabeto:
            destino = transicoes[(atual, s)]
            if destino not in alcancaveis:
                alcancaveis.append(destino)
                fila.append(destino)

    # mantém só os alcançáveis
    novos_estados = []
    for e in estados:
        if e in alcancaveis:
            novos_estados.append(e)

    novos_finais = []
    for e in finais:
        if e in alcancaveis:
            novos_finais.append(e)

    novas_trans = {}
    for chave in transicoes:
        if chave[0] in alcancaveis:
            novas_trans[chave] = transicoes[chave]

    return novos_estados, novos_finais, novas_trans


def minimizar(estados, alfabeto, inicial, finais, transicoes):
    estados, finais, transicoes = remover_inalcancaveis(estados, alfabeto, inicial, finais, transicoes)
    n = len(estados)

    # marcados = pares de estados distinguíveis, sempre na ordem da lista de estados
    marcados = []

    # passo 1: um final e um não final já são distinguíveis
    for i in range(n):
        for j in range(i + 1, n):
            if (estados[i] in finais) != (estados[j] in finais):
                marcados.append((estados[i], estados[j]))

    # passo 2: se com algum símbolo o par vai pra um par já marcado, ele também é marcado
    mudou = True
    while mudou:  # repete até uma passada inteira sem marcar nada novo
        mudou = False
        for i in range(n):
            for j in range(i + 1, n):
                p = estados[i]
                q = estados[j]
                if (p, q) in marcados:
                    continue
                for s in alfabeto:
                    dp = transicoes[(p, s)]
                    dq = transicoes[(q, s)]
                    # o par de destino pode estar guardado em qualquer ordem
                    if dp != dq and ((dp, dq) in marcados or (dq, dp) in marcados):
                        marcados.append((p, q))
                        mudou = True
                        break

    # o que sobrou sem marcar é equivalente: cada estado vira o primeiro da sua classe
    representante = {}
    for i in range(n):
        e = estados[i]
        representante[e] = e
        for j in range(i):
            outro = estados[j]
            if (outro, e) not in marcados:
                representante[e] = representante[outro]
                break

    # monta o autômato novo só com os representantes
    novos_estados = []
    for e in estados:
        if representante[e] == e:
            novos_estados.append(e)

    novo_inicial = representante[inicial]

    novos_finais = []
    for e in novos_estados:
        if e in finais:
            novos_finais.append(e)

    novas_trans = {}
    for e in novos_estados:
        for s in alfabeto:
            novas_trans[(e, s)] = representante[transicoes[(e, s)]]

    return novos_estados, novo_inicial, novos_finais, novas_trans