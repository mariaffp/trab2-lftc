# Minimização de AFD

Trabalho de Linguagens Formais e Teoria da Computação. O programa lê um AFD de um arquivo `.txt`, minimiza e mostra o autômato original e o mínimo.

## Como rodar

Precisa só do Python 

```
python src/main.py
```

O menu lista os arquivos da pasta `exemplos/`. Dá para escolher pelo número ou digitando o nome (com ou sem `.txt`).

## Formato do arquivo

Um cabeçalho com 4 linhas nesse formato mais simples que escolhemos, e depois uma transição por linha no formato `origem simbolo destino`:

```
estados: q0 q1 q2 q3 q4 q5
alfabeto: a b
inicial: q0
finais: q3
q0 a q1
q0 b q2
...
```

O AFD precisa ser completo: todo estado tem que ter uma transição para cada símbolo do alfabeto. Senão o programa avisa qual está faltando.

## Estrutura

- `src/automato.py`: lê o arquivo, valida e imprime o autômato.
- `src/minimizador.py`: remove os estados inalcançáveis e minimiza.
- `src/main.py`: o menu, parecido com o que fizemos em lftc 1.
- `exemplos/`: arquivos de teste.

## Como minimiza

1. Remove os estados que não dá para alcançar a partir do inicial.
2. Usa o preenchimento de tabela: começa marcando como distinguíveis os pares com um estado final e um não final. Depois repete: se um par, com algum símbolo, vai parar em um par já marcado, ele também é marcado. Para quando uma passada inteira não marca nada novo.
3. Os pares que ficaram sem marca são equivalentes e viram um estado só. Cada classe fica com o nome do primeiro estado dela.

## Limitações e possíveis otimizações em aberto para minha dupla 👍

- Só AFD, ainda não aceita AFND.
- Não aceita AFD incompleto.
- Estados e símbolos são separados por espaço, então os nomes não podem ter espaço.
- Outros possíveis erros como o primeiro que não enxergamos