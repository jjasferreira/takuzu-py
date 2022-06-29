# takuzu.py: Projeto de Inteligência Artificial 2021/2022
# Grupo 07:
# 99251 João Nuno Cardoso
# 99259 José João Ferreira

import numpy as np
import sys

from search import (
    Problem,
    Node,
    depth_first_tree_search,
    greedy_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board: "Board", last):
        self.board = board
        self.id = TakuzuState.state_id
        self.last = last
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, array, dim, empty_cells, row_tally, col_tally):
        self.array = array
        self.dim = dim
        self.empty_cells = empty_cells
        # Listas de listas de dimensão 2 que contêm o número de 0's e 1's, respetivamente
        self.row_tally = row_tally
        self.col_tally = col_tally

    def __repr__(self):
        res = ""
        for i in range(self.dim):
            for j in range(self.dim):
                res += str(self.array[i, j])
                if j < self.dim - 1:
                    res += "\t"
            if i < self.dim - 1:
                res += "\n"
        return res

    def get_row(self, row: int) -> tuple:
        return tuple(self.array[row, : self.dim])

    def get_column(self, col: int) -> tuple:
        return tuple(self.array[: self.dim, col])

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.array[row, col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        v1 = self.array[row + 1, col] if (row < self.dim - 1) else (None)
        v2 = self.array[row - 1, col] if (row > 0) else (None)
        return (v1, v2)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        v1 = self.array[row, col - 1] if (col > 0) else (None)
        v2 = self.array[row, col + 1] if (col < self.dim - 1) else (None)
        return (v1, v2)

    def two_numbers(self, row: int, col: int, mode) -> tuple:
        """Devolve os dois valores imediatamente abaixo, acima, à esquerda ou à direita,
        dependendo da string argumento."""
        if mode == "below":
            v1 = self.array[row + 2, col] if (row < self.dim - 2) else (None)
            v2 = self.array[row + 1, col] if (row < self.dim - 1) else (None)
        elif mode == "above":
            v1 = self.array[row - 1, col] if (row > 0) else (None)
            v2 = self.array[row - 2, col] if (row > 1) else (None)
        elif mode == "previous":
            v1 = self.array[row, col - 2] if (col > 1) else (None)
            v2 = self.array[row, col - 1] if (col > 0) else (None)
        elif mode == "following":
            v1 = self.array[row, col + 1] if (col < self.dim - 1) else (None)
            v2 = self.array[row, col + 2] if (col < self.dim - 2) else (None)
        return (v1, v2)

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        mat = []
        dim = int(input())
        for f in range(dim):
            mat.append([int(i) for i in input().split()])
        empty_cells = 0
        row_tally = []
        col_tally = []
        for i in range(dim):
            row_tally.append([0, 0])
            col_tally.append([0, 0])
        for i in range(dim):
            for j in range(dim):
                val = mat[i][j]
                if val != 2:
                    empty_cells += 1
                    row_tally[i][val] += 1
                    col_tally[j][val] += 1
        return Board(np.array(mat), dim, empty_cells, row_tally, col_tally)

    def apply_action(self, action):
        array = np.copy(self.array)
        array[action[0]][action[1]] = action[2]
        new_empty_cells = self.empty_cells - 1
        new_row_tally = []
        new_col_tally = []
        for i in range(self.dim):
            new_row_tally.append(self.row_tally[i].copy())
            new_col_tally.append(self.col_tally[i].copy())
        new_row_tally[action[0]][action[2]] += 1
        new_col_tally[action[1]][action[2]] += 1
        return Board(array, self.dim, new_empty_cells, new_row_tally, new_col_tally)


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board, None)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board = state.board
        dim = board.dim

        def check_two_numbers(state: TakuzuState, l: int, c: int, v: int):
            """Retorna verdadeiro se for possível colocar "v"
            na célula com linha "l" e coluna "c", com base nos dois valores
            imediatamente ao lado em todos os sentidos."""
            for m in ("previous", "following", "below", "above"):
                f = state.board.two_numbers(l, c, m)
                if f == (v, v):
                    return False
            return True

        def check_adjacent(state: TakuzuState, l: int, c: int, v: int):
            """Retorna verdadeiro se for possível colocar "v"
            na célula com linha "l" e coluna "c", com base nos
            valores adjacentes nas duas direções"""
            hori = state.board.adjacent_horizontal_numbers(l, c)
            vert = state.board.adjacent_vertical_numbers(l, c)
            if hori == (v, v) or vert == (v, v):
                return False
            return True

        # 01. Caso em que analisamos linhas e colunas na sua totalidade
        # Por cada linha
        row_t = board.row_tally
        for i in range(dim):
            zeros = row_t[i][0]
            ones = row_t[i][1]
            # Tabuleiro inválido se um dos números estiver preenchido para lá do número máximo
            if zeros >= dim / 2 + 1 or ones >= dim / 2 + 1:
                return []
            # Se só falta preencher uma célula
            if zeros + ones == dim - 1:
                for j in range(dim):
                    if board.get_number(i, j) == 2:
                        p = j
                # Se há um valor em maior número
                if zeros - ones != 0:
                    v = 1 if (zeros > ones) else (0)
                    if check_adjacent(state, i, p, v) and check_two_numbers(
                        state, i, p, v
                    ):
                        return [(i, p, v)]
                    else:
                        return []
            # Se um dos números já está maximizado
            elif zeros >= dim / 2 or ones >= dim / 2:
                for j in range(dim):
                    n = board.get_number(i, j)
                    # Encontrar primeira célula vazia
                    if n == 2:
                        # Tentar atribuir-lhe o valor em menor número
                        v = 1 if (zeros > ones) else (0)
                        # Se for possível
                        if check_two_numbers(state, i, j, v) and check_adjacent(
                            state, i, j, v
                        ):
                            return [(i, j, v)]
                        # Caso contrário
                        else:
                            return []
        # Por cada coluna
        col_t = board.col_tally
        for i in range(dim):
            zeros = col_t[i][0]
            ones = col_t[i][1]
            # Tabuleiro inválido se um dos números estiver preenchido para lá do número máximo
            if zeros >= dim / 2 + 1 or ones >= dim / 2 + 1:
                return []
            # Se só falta preencher uma célula
            if zeros + ones == dim - 1:
                for j in range(dim):
                    if board.get_number(j, i) == 2:
                        p = j
                # Se há um valor em maior número
                if zeros - ones != 0:
                    v = 1 if (zeros > ones) else (0)
                    if check_adjacent(state, p, i, v) and check_two_numbers(
                        state, p, i, v
                    ):
                        return [(p, i, v)]
                    else:
                        return []
                # O caso em que o tabuleiro é ímpar e há um número igual de 1's e 0's
                # permite as duas jogadas, pelo que não vale a pena considerá-lo aqui

            # Se um dos números já está maximizado
            elif zeros >= dim / 2 or ones >= dim / 2:
                for j in range(dim):
                    n = board.get_number(j, i)
                    # Encontrar primeira célula vazia
                    if n == 2:
                        # Tentar atribuir-lhe o valor em menor número
                        v = 1 if (zeros > ones) else (0)
                        # Se for possível
                        if check_two_numbers(state, j, i, v) and check_adjacent(
                            state, j, i, v
                        ):
                            return [(j, i, v)]
                        # Caso contrário
                        else:
                            return []

        # 02. Caso em que temos 2 células consecutivas iguais
        modes = ("previous", "following", "below", "above")
        for i in range(dim):
            for j in range(dim):
                if board.get_number(i, j) == 2:
                    for m in modes:
                        t = board.two_numbers(i, j, m)
                        if t == (0, 0):
                            return [(i, j, 1)]
                        elif t == (1, 1):
                            return [(i, j, 0)]

        # 03. Caso em que vemos as células imediatamente adjacentes
        for i in range(dim):
            for j in range(dim):
                if board.get_number(i, j) == 2:
                    h = board.adjacent_horizontal_numbers(i, j)
                    v = board.adjacent_vertical_numbers(i, j)
                    # Se houver alguma dupla igual, a escolha é óbvia
                    if h == (0, 0) or v == (0, 0):
                        return [(i, j, 1)]
                    if h == (1, 1) or v == (1, 1):
                        return [(i, j, 0)]

        # 04. Caso em que nada sabemos e damos prioridade ao número menos presente na linha e coluna
        res = []
        for i in range(dim):
            for j in range(dim):
                if board.get_number(i, j) == 2:
                    if (row_t[i][0] > row_t[i][1] and col_t[j][0] >= col_t[j][1]) or (
                        row_t[i][0] >= row_t[i][1] and col_t[j][0] > col_t[j][1]
                    ):
                        return [(i, j, 1), (i, j, 0)]
                    elif (row_t[i][0] < row_t[i][1] and col_t[j][0] <= col_t[j][1]) or (
                        row_t[i][0] <= row_t[i][1] and col_t[j][0] < col_t[j][1]
                    ):
                        return [(i, j, 0), (i, j, 1)]
                    else:
                        return [(i, j, 0), (i, j, 1)]
        return res

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        board = state.board.apply_action(action)
        return TakuzuState(board, action)

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""

        board = state.board
        row_t = board.row_tally
        col_t = board.col_tally
        dim = board.dim
        # Se a soma de 0's e 1's para cada linha é menor que a dimensão do
        # tabuleiro, então o tabuleiro ainda tem células vazias
        for i in range(dim):
            if sum(row_t[i]) != dim:
                return False
        rows = set()
        cols = set()
        for i in range(dim):
            r = board.get_row(i)
            c = board.get_column(i)
            if r in rows or c in cols:
                return False
            else:
                if (
                    row_t[i][0] >= dim / 2 + 1
                    or row_t[i][1] >= dim / 2 + 1
                    or col_t[i][0] >= dim / 2 + 1
                    or col_t[i][1] >= dim / 2 + 1
                ):
                    return False
                rows.add(r)
                cols.add(c)
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para as procuras Greedy e A*."""
        board = node.state.board

        # Heurística 1: maior quanto maior for o número de células esparsamente preenchidas
        dim = board.dim
        c = 0
        for i in range(dim):
            for j in range(dim):
                for m in ("previous", "following", "below", "above"):
                    t = board.two_numbers(i, j, m)
                    for value in t:
                        if value == 2:
                            c += 1
        return c / dim**2

        """
        # Heurística 2: devolve o número de células com o mesmo
        # valor na linha e na coluna da última ação do tabuleiro
        last = node.state.last
        if last != None:
            return board.row_tally[last[0]][last[2]] + board.col_tally[last[1]][last[2]]
        return 0
        """


if __name__ == "__main__":  # Função main

    # Resolução do problema
    board = Board.parse_instance_from_stdin()
    dim = board.dim
    problem = Takuzu(board)
    c = 0
    for i in range(dim):
        c += sum(board.row_tally[i])
    # Se o número de células preenchidas < metade, aplicar Greedy
    if c < (dim**2) / 2:
        goal_node = greedy_search(problem, problem.h)
    # Caso contrário, aplicar a procura DFS
    else:
        goal_node = depth_first_tree_search(problem)
    print(goal_node.state.board)
