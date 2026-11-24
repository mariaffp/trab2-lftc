import os 

from automato import ler_automato, imprimir_automato
from minimizador import minimizar

# pasta exemplos
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "exemplos")


def analisar(caminho):
    try:  # tenta ler o arquivo
        estados, alfabeto, inicial, finais, transicoes = ler_automato(caminho)
    except (OSError, ValueError) as e:
        print(f"erro: {e}")  # mostra a mensagem em vez de quebrar o programa
        return

    print("\nAutômato original:")
    imprimir_automato(estados, alfabeto, inicial, finais, transicoes)

    m_estados, m_inicial, m_finais, m_trans = minimizar(estados, alfabeto, inicial, finais, transicoes)

    print("\nAutômato mínimo:")
    imprimir_automato(m_estados, alfabeto, m_inicial, m_finais, m_trans)
    print(f"\nEstados: {len(estados)} -> {len(m_estados)}")


def escolher_arquivo():
    arquivos = sorted(f for f in os.listdir(PASTA) if f.endswith(".txt"))  # só os .txt, em ordem

    if arquivos:
        print("\nArquivos em exemplos/:")
        for i, nome in enumerate(arquivos, 1):  # numera a partir de 1
            print(f"  {i}. {nome}")
    else:
        print("\nA pasta exemplos/ está vazia.")

    resp = input("Número ou nome do arquivo (Enter para voltar): ").strip()
    if not resp:
        return None
    if resp.isdigit() and 1 <= int(resp) <= len(arquivos):
        return os.path.join(PASTA, arquivos[int(resp) - 1])  # -1 porque a lista começa no 0

    # procura dentro de exemplos
    nome = resp if resp.endswith(".txt") else resp + ".txt"
    candidato = os.path.join(PASTA, nome)
    if os.path.exists(candidato):
        return candidato

    return resp  # senão, trata como caminho completo


def menu():
    while True: 
        print("\n1. Escolher um arquivo")
        print("0. Sair")
        op = input("Opção: ").strip()

        if op == "0":
            break
        elif op == "1":
            caminho = escolher_arquivo()
            if caminho:  # None (cancelou) conta como falso
                analisar(caminho)
        else:
            print("Opção inválida.")


if __name__ == "__main__":  # só roda o menu se este arquivo for executado diretamente
    menu()