# takuzu.py: Projeto de Inteligência Artificial 2021/2022
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

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    def __init__(self, array, dim, row_tally, col_tally):
        self.array = array
        self.dim = dim
        # Listas de listas de dimensão 2 que contêm o número de 0's e 1's, respetivamente
        self.row_tally = row_tally
        self.col_tally = col_tally

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

    def get_column(self, col: int) -> tuple:
        return tuple(self.array[:self.dim, col])

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

        row_tally = []
        col_tally = []
        for i in range(dim):
            row_tally.append([0, 0])
            col_tally.append([0, 0])
        for i in range(dim):
            for j in range(dim):
                val = mat[i][j]
                if val != 2:
                    row_tally[i][val] += 1
                    col_tally[j][val] += 1

        return Board(np.array(mat), dim, row_tally, col_tally)

    def apply_action(self, action):
        array = np.copy(self.array)
        array[action[0]][action[1]] = action[2]
        new_row_tally = self.row_tally.copy()
        new_col_tally = self.col_tally.copy()
        new_row_tally[action[0]][action[2]] += 1
        new_col_tally[action[1]][action[2]] += 1

        return Board(array, self.dim, new_row_tally, new_col_tally)

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
        dim = board.dim
        row_tally = board.row_tally
        col_tally = board.col_tally
        
        def check_two_numbers(self, state: TakuzuState, l: int, c: int, v: int):
            """Retorna verdadeiro se for possível colocar "v"
            na célula com linha "l" e coluna "c", com base nos dois valores
            imediatamente ao lado em todos os sentidos."""
            for m in ("previous", "following", "below", "above"):
                f = state.board.two_numbers(l, c, m)
                if (f == (v, v)):
                    return False
            return True
    
        def check_adjacent(self, state: TakuzuState, l: int, c: int, v: int):
            """Retorna verdadeiro se for possível colocar "v"
            na célula com linha "l" e coluna "c", com base nos
            valores adjacentes nas duas direções"""
            hori = state.board.adjacent_horizontal_numbers(l, c)
            vert = state.board.adjacent_vertical_numbers(l, c)
            if (hori == (v, v) or vert == (v, v)):
                return False
            return True

        # 01. Caso em que analsamos linhas e colunas na sua totalidade
        # Por cada linha
        for i in range(dim):
            zeros = row_tally[i][0]
            ones = row_tally[i][1]
            # IDK: provisório?
            if (zeros >= dim/2 + 1 or ones >= dim/2 + 1):
                print("Olha! \n Deu merda!")
                return []
            # Se só falta preencher uma célula
            if (zeros + ones == dim - 1):
                for j in range(dim):
                    if (board.get_number(i, j) == 2):
                        p = j
                # Se há um valor em maior número
                if (zeros - ones != 0):
                    v = 1 if (zeros > ones) else (0)
                    return [(i, p, v)]
            # Se um dos números já está maximizado
            elif (zeros >= dim/2 or ones >= dim/2):
                for j in range(dim):
                    n = board.get_number(i, j)
                    # Encontrar primeira célula vazia
                    if (n == 2):
                        # Tentar atribuir-lhe o valor em menor número
                        v = 1 if (zeros > ones) else (0)
                        # Se for possível
                        if (check_two_numbers(self, state, i, j, v) and check_adjacent(self, state, i, j, v)):
                            return [(i, j, v)]
                        # Caso contrário
                        else:
                            return []
        # Por cada coluna                
        for i in range(dim):
            zeros = col_tally[i][0]
            ones = col_tally[i][1]
            # IDK: provisório?
            if (zeros >= dim/2 + 1 or ones >= dim/2 + 1):
                print("Olha! \n Deu merda!")
                return []
            # Se só falta preencher uma célula
            if (zeros + ones == dim - 1):
                for j in range(dim):
                    if (board.get_number(j, i) == 2):
                        p = j
                # Se há um valor em maior número
                if (zeros - ones != 0):
                    v = 1 if (zeros > ones) else (0)
                    return [(p, i, v)]
                # O caso em que o tabuleiro é ímpar e há um número igual de 1's e 0's
                # permite as duas jogadas, pelo que não vale a pena considerá-lo aqui
                
            # Se um dos números já está maximizado
            elif (zeros >= dim/2 or ones >= dim/2):
                for j in range(dim):
                    n = board.get_number(j, i)
                    # Encontrar primeira célula vazia
                    if (n == 2):
                        # Tentar atribuir-lhe o valor em menor número
                        v = 1 if (zeros > ones) else (0)
                        # Se for possível
                        if (check_two_numbers(self, state, j, i, v) and check_adjacent(self, state, j, i, v)):
                            return [(j, i, v)]
                        # Caso contrário
                        else:
                            return []

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
        dim = board.dim
        # Se a some de 0's e 1's para cada linha é menor que a dimensão do
        # tabuleiro, então o tabuleiro ainda tem células vazias
        for i in range(dim):
            if sum(board.row_tally[i]) != dim:
                return False
        rows = set()
        cols = set()
        even = (dim % 2 == 0)

        def valid_section(section, even):
            """Decide se uma linha ou coluna de um tabuleiro é válida"""
            previous = None
            # Número de jogadas sucessivas
            state = 0 # Conta o número sucessivo de um tipo de peça
            sum = 0 # Balanço
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
            if r in rows or c in cols:        
                return False
            else:
                if not valid_section(r, even) or not valid_section(c, even):            
                    return False
                rows.add(r)
                cols.add(c)
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