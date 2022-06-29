# Relatório do Projeto de Inteligência Artificial (LEIC-A 2021/2022)

Grupo AL007 - João Cardoso (99251) e José João Ferreira (99259)

---

## Implementação

A nossa implementação tem como foco a restrição de ações, com base nas regras do jogo, de forma a que o _branching factor_ seja o menor possível. Para tal, retornamos, no método `Takuzu.actions`, as ações que forçosamente têm que ser tomadas, como preencher uma célula em que as duas adjacentes têm o mesmo valor com o valor oposto, preencher uma célula que venha no seguimento de duas outras contendo o mesmo valor com o valor oposto, ou preencher a última célula de uma linha/coluna com o valor que assegura que o número total de valores para essa fila é o correto. Para a última regra do jogo - ter todas as linhas/colunas distintas - dependemos do _goal_test_, e por isso esta regra não é contemplada no método. Quando não há nenhuma ação necessária, dadas as regras do jogo, devolvemos apenas duas ações, referentes à mesma posição, por forma a evitar estados repetidos (como a ordem das ações não interessa, podemos reduzir cada nível a uma escolha binária, no pior caso). Assim, o _branching factor_ encontra-se entre 1 e 2, mas muito próximo de 1, o que assegura uma execução extremamente rápida, mesmo para tabuleiros grandes e/ou esparsamente preenchidos.

## Heurísticas

Numa primeira fase de implementação, impúnhamos menos restrições nas ações, pelo que se tornava relevante decidir em que posição fazer a próxima jogada. Por forma a falhar na árvore de procura mais cedo, decidimos usar a nossa heurística para dar prioridade a jogadas que estivessem mais próximas de outras, já que as regras do jogo incidem sobretudo em situações de proximidade entre células (adjacentes, seguidas, ou na mesma linha coluna). Para tal, atribuíamos a cada tabuleiro possível uma _score_ com base no quão "compacto" ele era, percorrendo todas as células, somando o número de células vazias adjacentes para cada célula. Note-se que esta heurística não é admissível (muito menos completa), pois para um tabuleiro do "tipo xadrez", com células preenchidas alternadamente, irá contar todas as células vazias duas ou mais vezes, retornando um número superior ao de células vazias, que coincide com o número de passos até à solução (é um caso trivial de resolver).
No entanto, ao restringir as ações como acima referido, esta heurística deixou de fazer sentido, já que nos casos em que havia uma escolha entre duas ações, estas duas ações eram referentes à mesma posição. Sendo assim, a única variável relevante é o número a preencher, pelo que implementámos uma heurística que calcula, para a posição da última ação do estado, o número de células da mesma linha e coluna que têm o mesmo valor que o da ação. Assim, prioritizamos ações em que o valor a preencher é o que está em menor frequência na linha/coluna. Esta heurística não é admissível (nem completa), pois no caso em que só falta preencher uma célula, ela irá retornar o número de valores da mesma linha e coluna da última posição, que irá ser maior que 1, que é o número de passos até chegar à solução.

## Análise dos resultados

Todas as implementações discutidas seguidamente são corretas, ainda que algumas não cheguem à solução em tempo útil.
Os resultados dos testes sugerem que uma procura (01.) sem qualquer tipo de filtragem das ações é imensamente ineficiente. Ainda assim, a heurística de escolha de posição de ação parece melhorar consideravelmente o desempenho, o que indica que a estratégia de escolher jogadas mais próximas umas das outras é benéfica.
No caso em que só há duas ações possíveis por nível (02.), os resultados são bastante melhores, e a heurística 2 torna a procura A\* ligeiramente mais eficiente que a BFS, ainda que a DFS mostre ser a mais eficiente. Curiosamente, a heurística permite à procura gananciosa encontrar a solução com o menor número de nós expandidos possível.
Na implementação final (03.), a restrição apertada das ações significa que para quase todos os níveis há apenas uma ação a escolher, pelo que os diferentes tipos de procura produzem resultados muito semelhantes. Uma análise do teste privado esparso revela resultados que contrariam alguns dos pressupostos que tínhamos. Por um lado, assumíamos que a heurística 1 não iria ter efeito num cenário em que só há no máximo duas ações.
Contudo, pensamos que como a procura gananciosa contabiliza o valor de estados mais acima na sua execução, possa estar a abandonar ramos que se tornam demasiado esparsos. A heurística que se baseia apenas no valor da célula parece oferecer uma pequena melhoria face à procura em largura primeiro, mas não o suficiente para justificar o seu uso face a uma DFS. Note-se, também, que estes resultados foram obtidos após a última submissão no Mooshak, em que supúnhamos que uma procura gananciosa funcionaria melhor para um tabuleiro esparso com a heurística h2, quando os testes parecem indicar que a h1 é mais adequada.

---

### Heurística 1

```py
board = node.state.board
dim = board.dim
c = 0
for i in range(dim):
    for j in range(dim):
        for m in ("previous", "following", "below", "above"):
            t = board.two_numbers(i, j, m)
            for value in t:
                if value == 2:
                    c += 1
return (c / dim**2)
```

### Heurística 2

```py
last = node.state.last
row_t = board.row_tally
col_t = board.col_tally
if last_action != None:
    return row_t[last[0]][last[2]] + col_t[last[1]][last[2]]
return 0
```

---

## Tabelas do tempo de execução e nós gerados e expandidos ao longo do desenvolvimento do projeto

Os tempos de execução foram obtidos com recurso à ferramenta [`hyperfine`](https://github.com/sharkdp/hyperfine), com 5 _warm ups_. O resultado, para cada algoritmo considerado em cada tabela, é a média entre 30 _runs_.

### 01. Todas as ações possíveis (s/ restrições)

- **DIM 4 (7)**, \*Procuras Greedy e A-Star c/ Heurística 1

| Algoritmo    | **Tempo de execução**  | **Nós gerados**  | **Nós expandidos**  |
| ------------ | ---------------------- | ---------------- | ------------------- |
| **BFS**      | 19.792 s               | 1063622          | 422393              |
| **DFS**      | 1.637 s                | 76627            | 76627               |
| **Greedy**\* | 666.8 ms               | 7030             | 6984                |
| **A-Star**\* | > 5 min                | -                | -                   |

- **DIM 12 (79)**, \*Procuras Greedy e A-Star c/ Heurística 1

| Algoritmo    | **Tempo de execução**  | **Nós gerados** | **Nós expandidos**  |
| ------------ | ---------------------- | --------------- | ------------------- |
| **BFS**      | > 1 hr                 | -               | -                   |
| **DFS**      | > 1 hr                 | -               | -                   |
| **Greedy**\* | > 1 hr                 | -               | -                   |
| **A-Star**\* | > 1 hr                 | -               | -                   |

---

### 02. Árvore binária de ações (c/ restrições)

- **DIM 4 (7)**, \*Procuras Greedy e A-Star c/ Heurística 2

| Algoritmo    | **Tempo de execução**  | **Nós gerados**  | **Nós expandidos**  |
| ------------ | ---------------------- | ---------------- | ------------------- |
| **BFS**      | 182.8 ms               | 254              | 169                 |
| **DFS**      | 181.6 ms               | 176              | 173                 |
| **Greedy**\* | 178.2 ms               | 14               | 7                   |
| **A-Star**\* | 185.9 ms               | 230              | 131                 |

- **DIM 12 (79)**, \*Procuras Greedy e A-Star c/ Heurística 2

| Algoritmo    | **Tempo de execução**  | **Nós gerados** | **Nós expandidos**  |
| ------------ | ---------------------- | --------------- | ------------------- |
| **BFS**      | > 30 min               | -               | -                   |
| **DFS**      | > 30 min               | -               | -                   |
| **Greedy**\* | > 30 min               | -               | -                   |
| **A-Star**\* | > 30 min               | -               | -                   |

---

### 03. Ações óbvias e verificadas: final (c/ restrições)

- **DIM 4 (7)**, \*Procuras Greedy e A-Star c/ Heurística 2

| Algoritmo    | **Tempo de execução**  | **Nós gerados** | **Nós expandidos**  |
| ------------ | ---------------------- | --------------- | ------------------- |
| **BFS**      | 178.1 ms               | 7               | 7                   |
| **DFS**      | 176.2 ms               | 7               | 7                   |
| **Greedy**\* | 177.5 ms               | 7               | 7                   |
| **A-Star**\* | 178.1 ms               | 7               | 7                   |

- **DIM 12 (79)**, \*Procuras Greedy e A-Star c/ Heurística 2

| Algoritmo    | **Tempo de execução**  | **Nós gerados**  | **Nós expandidos** |
| ------------ | ---------------------- | ---------------- | ------------------ |
| **BFS**      | 189.7 ms               | 85               | 85                 |
| **DFS**      | 189.0 ms               | 82               | 81                 |
| **Greedy**\* | 191.8 ms               | 85               | 85                 |
| **A-Star**\* | 194.1 ms               | 85               | 85                 |

- **DIM 31 (180)**, \*Procuras Greedy e A-Star c/ Heurística 2

| Algoritmo    | **Tempo de execução**  | **Nós gerados** | **Nós expandidos**  |
| ------------ | ---------------------- | --------------- | ------------------- |
| **BFS**      | 241.4 ms               | 180             | 180                 |
| **DFS**      | 239.6 ms               | 180             | 180                 |
| **Greedy**\* | 240.9 ms               | 180             | 180                 |
| **A-Star**\* | 241.7 ms               | 180             | 180                 |

- **DIM 12 (144)**, \*Procuras Greedy e A-Star c/ Heurística 1

| Algoritmo   | **Tempo de execução**   | **Nós gerados**  | **Nós expandidos**   |
| ----------- | ----------------------- | ---------------- | -------------------- |
| **BFS**     | 568.6 ms                | 6856             | 6860                 |
| **DFS**     | 478.2 ms                | 6049             | 6054                 |
| **Greedy**  | 393.4 ms                | 925              | 939                  |
| **A-Star**  | 3257.6 ms               | 6855             | 6860                 |

- **DIM 12 (144)**, \*Procuras Greedy e A-Star c/ Heurística 2

| Algoritmo   | **Tempo de execução**   | **Nós gerados**  | **Nós expandidos**   |
| ----------- | ----------------------- | ---------------- | -------------------- |
| **BFS**     | 550.7 ms                | 6856             | 6860                 |
| **DFS**     | 465.9 ms                | 6049             | 6054                 |
| **Greedy**  | 1013.6 ms               | 6839             | 6845                 |
| **A-Star**  | 967.1 ms                | 6856             | 6860                 |

---

## Testes utilizados

| Nome              | **Ficheiro**  | **Descrição do tabuleiro**                      |
| ----------------- | ------------- | ----------------------------------------------- |
| **DIM 4 (7)**     | t_04_007.in   | Dimensão 4 com 7 casas por preencher (≈44%)     |
| **DIM 12 (79)**   | t_12_079.in   | Dimensão 12 com 79 casas por preencher (≈55%)   |
| **DIM 31 (180)**  | t_31_180.in   | Dimensão 31 com 180 casas por preencher (≈19%)  |
| **DIM 12 (114)**  | t_12_114.in   | Dimensão 12 com 114 casas por preencher (≈79%)  |
