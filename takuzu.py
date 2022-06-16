# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 07:
# 99251 João Nuno Cardoso
# 99259 José João Ferreira

import numpy as np

import sys
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

    def __init__(self, board):
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
    def __init__(self, array, dim, empty_cells):
        self.state = array
        self.dim = dim
        self.empty_cells = empty_cells

    def __repr__(self):
        res = ""
        for i in range(self.dim):
            for j in range(self.dim):
                res += str(self.state[i, j]) + "\t"
            res += "\n"
        return res
    
    def get_row(self, row: int) -> tuple:
        return tuple(self.state[row, :self.dim])

    def get_column(self, column: int) -> tuple:
        return tuple(self.state[:self.dim, column])

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.state[row, col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        v1 = self.state[row + 1, col] if (row < self.dim - 1) else (None)
        v2 = self.state[row - 1, col] if (row > 0) else (None) 
        return (v1, v2)
    
    def two_below_vertical_numbers(self, row: int, col: int) -> tuple:
        """Devolve os dois valores consecutivos imediatamente abaixo."""
        v1 = self.state[row + 2, col] if (row < self.dim - 2) else (None)
        v2 = self.state[row + 1, col] if (row < self.dim - 1) else (None)
        return (v1, v2)

    def two_above_vertical_numbers(self, row: int, col: int) -> tuple:
        """Devolve os dois valores consecutivos imediatamente acima."""
        v1 = self.state[row - 1, col] if (row > 0) else (None) 
        v2 = self.state[row - 2, col] if (row > 1) else (None) 
        return (v1, v2)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        v1 = self.state[row, col - 1] if (col > 0) else (None) 
        v2 = self.state[row, col + 1] if (col < self.dim - 1) else (None)
        return (v1, v2)
    
    def two_previous_horizontal_numbers(self, row: int, col: int) -> tuple:
        """Devolve os dois valores consecutivos imediatamente à esquerda."""
        v1 = self.state[row, col - 2] if (col > 1) else (None)
        v2 = self.state[row, col - 1] if (col > 0) else (None)
        return (v1, v2)

    def two_following_horizontal_numbers(self, row: int, col: int) -> tuple:
        """Devolve os dois valores consecutivos imediatamente à direita."""
        v1 = self.state[row, col + 1] if (col < self.dim - 1) else (None)
        v2 = self.state[row, col + 2] if (col < self.dim - 2) else (None)
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

        empty_cells = 0
        for i in range(dim):
            for j in range(dim):
                if mat[i][j] == 2:
                    empty_cells+=1

        return Board(np.array(mat), dim, empty_cells)

    def apply_action(self, action):
        array = self.state
        array[action[0]][action[1]] = action[2]
        return Board(array, self.dim, self.empty_cells - 1)

    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # NEW:
        self.current = board
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        res = []
        """
        - Iterar pelas células,
        - Avaliar 2 antes e 2 depois
        - 
        """
        board = state.board
        for i in range(board.dim):
            for j in range(board.dim):
                if board.get_number(i, j) == 2:
                    h = set()
                    hn = board.adjacent_horizontal_numbers(i, j)
                    if (hn == (1, 1)):
                        h.add(0)
                    elif (hn == (0,0)):
                        h.add(1)
                    else:
                        h.update([0,1])
                    v = set()
                    vn = board.adjacent_vertical_numbers(i, j)
                    if (vn == (1, 1)):
                        v.add(0)
                    elif (vn == (0,0)):
                        v.add(1)
                    else:
                        v.update([0,1])
                    s = h.intersection(v)
                    if (len(s) != 0):
                        for k in s:
                            res.append([i, j, k])
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
        
        board = state.get_board()
        if board.empty_cells != 0:
            print("1")
            return False
        rows = set()
        columns = set()
        dim = board.dim
        even = (dim % 2 == 0)

        def valid_section(section, even):
            """Decide se uma linha ou coluna de um tabuleiro é válida"""
            previous = None
            # Número de jogadas sucessivas
            state = 0
            sum = 0
            for i in range(dim):
                print(i , "State:" , " " , state , "\n")
                val = section[i]
                print(val , "\n")
                if val == 2:
                    print("2")
                    return False
                sum += -1 if (val == 1) else -1
                if val != previous:
                    state = 1
                else:
                    if state == 2:
                        print("3")
                        return False
                    state += 1
                previous = val
                if i == (dim-1) and abs(state) == 1 and even:
                    print("4")
                    return False
            return True

        for i in range(dim):
            r = board.get_row(i)
            c = board.get_column(i)
            print(str(r) + str(c))
            if r in rows or c in columns:
                print("5")
                return False
            else:
                if not valid_section(r, even) or not valid_section(c, even):
                    print("6")
                    return False
                rows.add(r)
                columns.add(c)
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        # J: aceder ao node.state para ver o estado
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

    # Exemplo 2:
    board = Board.parse_instance_from_stdin()
    print("Initial:\n", board, sep="")
    problem = Takuzu(board)
    initial_state = TakuzuState(board)
    print(problem.goal_test(initial_state))
