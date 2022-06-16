# takuzu-py

Projeto para a disciplina de Inteligência Artificial (LEIC-A @ IST 21/22)
Um programa em Python 3.8 que resolve o problema _Takuzu_ usando técnicas "A.I." de busca

---

## Dúvidas

- **_JOTA_**: O que é o Node, no search.py? É uma abstração do TazukuState? E onde é que implementamos as funções expand? Temos que alterar o Node para ter um state com o estado do tabuleiro? Como é que integramos o Node no takuzu.py?

  > **_CARROTT_**: Não é suposto alterar o search.py, todo o código que desenvolverem tem de estar no takuzu.py. Podem meter prints nas funções do search.py para ajudar a fazer debug, mas no mooshak vocês só submetem o takuzu.py que depois vai chamar o search.py original. Têm de definir as classes Board, TakuzuState e Takuzu. - O Board é suposto ter a representação interna do tabuleiro e as operações sobre o tabuleiro que considerarem necessárias. - O TakuzuState vai ter este Board como atributo e serve como uma abstração para os nós nas procuras do search.py. - No Takuzu vais definir os métodos necessários para a procura. O actions é chamado internamente pelo expand no search.py e o h é chamado nas procuras A\* e gananciosa, por exemplo.

- **_JOTA_**: Dado um tabuleiro inicial, no método 'actions', devemos devolver a lista com todas as ações possíveis, fazer uma avaliação inicial e retirar aquelas que vão inevitavelmente conduzir a estados falhados usando as funções que retornam os números adjacentes horizontal e verticalmente ou fazer ainda mais do que isso e avaliar todas as restrições do problema?

  > **_CARROTT_**: O actions deve devolver as ações que acharem melhor para resolver o problema. **Não têm necessariamente que devolver todos os preenchimentos possíveis**, podem filtrar as opções como bem entenderem e cortar caminhos assim que uma ação levou a um estado inválido.
  >
  > > **_JOTA IDK_**: Pôr as ações que têm inevitavelmente que ser feitas (por exemplo 0,\_,0: mais cedo ou mais tarde, vamos ter que pôr um 1 ali e vamos, por isso mais vale dar prioridade a esta) no início da fila???

- **_JOTA_**: O método 'h' da classe Takuzu percorre a lista de ações e atribui um número para cada uma?

  > **_CARROTT_**: Para o h podem definir uma heurística com base nas ações do tabuleiro atual, mas **podem também tentar fazer uma análise diferente dos valores que já estão (ou faltam) no tabuleiro** e extrair uma heurística daí, por exemplo. Em princípio, não deves precisar da heurística para ter o 15 no mooshak, portanto aconselho a preocupares-te mais em restringir o actions o máximo possível.
  >
  > > **_JOTA IDK_**: Então talvez não se calcula a heurística das ações seguintes e calcula-se antes apenas a do estado atual, com base nas restrições???

- **_JOTA_**: É suposto implementarmos ideias dos algoritmos de CSPs (i.e.: Procura com Retrocesso, Heurística dos Valores Remanescentes Mínimos / do Maior Grau)?
  > **_CARROTT_**: Desde que esteja dentro do template, podem modelar o problema como bem entenderem. Usar as mesmas ideias (e.g. **DFS**, **heurísticas**, etc.) que os CSPs é até ideal para resolver o problema. Não devem (nem precisam de) implementar um pseudo CSP _solver_ de raiz.

---

## TODO List:

    Lista de recursos a implementar

- [ ] apply action
- [ ] goal state
- [ ] asd

---

## Pseudocode

```python
def function(asd):
```

---

## Report text:

    Texto a escrever ao longo do desenvolvimento do projeto para utilizar no relatório de entrega
