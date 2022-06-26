# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 07:
# 99251 João Nuno Cardoso
# 99259 José João Ferreira

import numpy as np

import sys

from tomlkit import string
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board: 'Board'):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    def get_board(self):
        return self.board
    # TODO: outros metodos da classe

class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    def __init__(self, array, dim, empty_cells_line, empty_cells_column):
        self.array = array
        self.dim = dim
        self.empty_cells_line = empty_cells_line
        self.empty_cells_column = empty_cells_column

    def __repr__(self):
        res = ""
        for i in range(self.dim):
            for j in range(self.dim):
                res += str(self.array[i, j]) + "\t"
            if (i < self.dim - 1):
                res += "\n"
        return res
    
    def get_row(self, row: int) -> tuple:
        return tuple(self.array[row, :self.dim])

    def get_column(self, column: int) -> tuple:
        return tuple(self.array[:self.dim, column])

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
    
    def two_numbers(self, row: int, col: int, mode: string) -> tuple:
        """Devolve os dois valores imediatamente abaixo, acima, à esquerda ou à direita,
        dependendo da string argumento."""
        if (mode == "below"):
            v1 = self.array[row + 2, col] if (row < self.dim - 2) else (None)
            v2 = self.array[row + 1, col] if (row < self.dim - 1) else (None)
        elif (mode == "above"):
            v1 = self.array[row - 1, col] if (row > 0) else (None) 
            v2 = self.array[row - 2, col] if (row > 1) else (None) 
        elif (mode == "previous"):
            v1 = self.array[row, col - 2] if (col > 1) else (None)
            v2 = self.array[row, col - 1] if (col > 0) else (None)
        elif (mode == "following"):
            v1 = self.array[row, col + 1] if (col < self.dim - 1) else (None)
            v2 = self.array[row, col + 2] if (col < self.dim - 2) else (None)
        return (v1, v2)

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        mat = []
        dim = int(input())
        for foo in range(dim):
            # IDK: Isto faz split todas as iterações?
            mat.append([int(i) for i in input().split()])

        empty_cells_line = [dim] * dim
        empty_cells_column = [dim] * dim
        for i in range(dim):
            for j in range(dim):
                if mat[i][j] != 2:
                    empty_cells_line[i] -= 1
                    empty_cells_column[j] -= 1

        return Board(np.array(mat), dim, empty_cells_line, empty_cells_column)

    def apply_action(self, action):
        array = np.copy(self.array)
        array[action[0]][action[1]] = action[2]
        empty_cells_line_cp = self.empty_cells_line.copy()
        empty_cells_column_cp = self.empty_cells_column.copy()
        empty_cells_line_cp[action[0]] -= 1
        empty_cells_column_cp[action[1]] -= 1

        return Board(array, self.dim, empty_cells_line_cp, empty_cells_column_cp)

    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        modes = ("previous", "following", "below", "above")
        board = state.board
        empty_cells_line = state.board.empty_cells_line
        empty_cells_column = state.board.empty_cells_column

        # 01. Caso em que temos linhas/colunas com apenas 1 célula livre
        for i in range(board.dim):
            if empty_cells_line[i] == 1:
                sum = 0
                even = not board.dim % 2
                pos = 0
                for j in range(board.dim):
                    n = board.get_number(i, j)
                    if n == 2:
                        pos = j
                    else:
                        sum += 1 if (n == 1) else (-1)
                if even and sum == 1:
                    return [(i, pos, 0)]
                elif even and sum == -1:
                    return [(i, pos, 1)]
                elif not even and sum == 2:
                    return [((i, pos, 0))]
                elif not even and sum == -2:
                    return [((i, pos, 1))]
                elif not even and sum == 0:
                    return [(i, pos, 0), (i, pos, 1)]
            if empty_cells_column[i] == 1:
                sum = 0
                even = not board.dim%2
                pos = 0
                for j in range(board.dim):
                    n = board.get_number(j, i)
                    if n == 2:
                        pos = j
                    else:
                        sum += 1 if (n == 1) else (-1)
                if even and sum == 1:
                    return [(pos, i, 0)]
                elif even and sum == -1:
                    return [(pos, i, 1)]
                elif not even and sum == 2:
                    return [((pos, i, 0))]
                elif not even and sum == -2:
                    return [((pos, i, 1))]
                elif not even and sum == 0:
                    return [(pos, i, 0), (pos, i, 1)]

        # 02. Caso em que temos 2 células consecutivas iguais
        for i in range(board.dim):
            for j in range(board.dim):
                if board.get_number(i, j) == 2:
                    for m in modes:
                        f = board.two_numbers(i, j, m)
                        if (f == (0, 0) or f == (1, 1)):
                            if (f[0] == 0): v = 1
                            elif (f[0] == 1): v = 0
                            return [(i, j, v)]

        # 03. Caso em que vemos as células imediatamente adjacentes
        res = []
        for i in range(board.dim):
            for j in range(board.dim):
                if board.get_number(i, j) == 2:
                    h = set()
                    hn = board.adjacent_horizontal_numbers(i, j)
                    if (hn == (0, 0)): h.add(1)
                    elif (hn == (1, 1)): h.add(0)
                    else: h.update([0,1])
                    v = set()
                    vn = board.adjacent_vertical_numbers(i, j)
                    if (vn == (0, 0)): v.add(1)
                    elif (vn == (1, 1)): v.add(0)
                    else: v.update([0,1])
                    s = h.intersection(v)
                    l = len(s)
                    if (l == 1):
                        return [(i, j, s.pop())]
                    elif (l == 2):
                        for k in s:
                            res.append((i, j, k))
        return res

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        board = state.board.apply_action(action)
        return TakuzuState(board)

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        
        board = state.board
        if (sum(board.empty_cells_line) != 0):
            return False
        rows = set()
        columns = set()
        dim = board.dim
        even = (dim % 2 == 0)

        def valid_section(section, even):
            """Decide se uma linha ou coluna de um tabuleiro é válida"""
            previous = None
            # Número de jogadas sucessivas
            state = 0 # counts the number of successive pieces of any kind
            sum = 0 # balance between 
            values = {0:-1, 1:1}
            for i in range(dim):
                val = section[i]
                if val == previous: state += 1
                else: state = 1
                sum += values[val]
                if state == 3:
                    return False
                previous = val
            if even:
                return (sum==0)
            else:
                return (abs(sum) == 1)

        for i in range(dim):
            r = board.get_row(i)
            c = board.get_column(i)    
            if r in rows or c in columns:        
                return False
            else:
                if not valid_section(r, even) or not valid_section(c, even):            
                    return False
                rows.add(r)
                columns.add(c)
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":  # Função main
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    """
    # Exemplo 1:
    board = Board.parse_instance_from_stdin()
    print("Initial:\n", board, sep="")
    print(board.adjacent_vertical_numbers(3,3))
    print(board.adjacent_horizontal_numbers(3,3))
    print(board.adjacent_vertical_numbers(1,1))
    print(board.adjacent_horizontal_numbers(1,1))
    """

    """
    # Exemplo 2:
    board = Board.parse_instance_from_stdin()
    print("Initial:\n", board, sep="")
    problem = Takuzu(board)
    initial_state = TakuzuState(board)
    print(initial_state.board.get_number(2, 2))
    result_state = problem.result(initial_state, (2, 2, 1))
    print(result_state.board.get_number(2, 2))
    """
    """
    # Exemplo 3:
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    s0 = TakuzuState(board)
    print("Initial:\n", s0.board, sep="")
    s1 = problem.result(s0, (0, 0, 0))
    s2 = problem.result(s1, (0, 2, 1))
    s3 = problem.result(s2, (1, 0, 1))
    s4 = problem.result(s3, (1, 1, 0))
    s5 = problem.result(s4, (1, 3, 1))
    s6 = problem.result(s5, (2, 0, 0))
    s7 = problem.result(s6, (2, 2, 1))
    s8 = problem.result(s7, (2, 3, 1))
    s9 = problem.result(s8, (3, 2, 0))
    print("Is goal?", problem.goal_test(s9))
    print("Solution:\n", s9.board, sep="")
    """

    # Exemplo 4:
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    goal_node = depth_first_tree_search(problem)
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution: \n", goal_node.state.board, sep="")
    
    """
    # Exemplo NEW:
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    s0 = TakuzuState(board)
    print("Initial:\n", s0.board, sep="")
    s1 = problem.result(s0, (0, 0, 0))
    print("Initial:\n", s1.board, sep="")
    s2 = problem.result(s1, (0, 2, 1))
    print("Initial:\n", s2.board, sep="")
    print("Is goal?", problem.goal_test(s2))
    """

    """
    # Exemplo das Actions:
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    s0 = TakuzuState(board)
    print("Initial:\n", s0.board, sep="")
    print(problem.actions(s0))
    s1 = problem.result(s0, (0, 0, 0))
    print(s1.board)
    print(problem.actions(s1))
    s2 = problem.result(s1, (0, 1, 1))
    print(s2.board)
    print(problem.actions(s2))
    s3 = problem.result(s2, (1, 2, 0))
    print(s3.board)
    print(problem.actions(s3))
    """

    """
    # Resolução do problema
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    goal_node = depth_first_tree_search(problem)

    print(goal_node.state.board)
    """
