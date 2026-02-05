import copy

import numpy as np

class ConnectN:
    def __init__(self, rows=4, columns=5):
        self.EMPTY = 0
        self.P1 = 1
        self.P2 = 2
        self.rows = rows
        self.columns = columns

        self.next_player = self.P1
        self.flip_player = {self.P1: self.P2,self.P2: self.P1}

        self.board = np.zeros((self.columns, self.rows), dtype=int)

        self.winner = None

    def valid_move(self, col):
        return -1 < col < self.columns and self.board[col][self.rows - 1] == self.EMPTY

    def play(self, col):
        if not self.valid_move(col):
            raise ValueError("Column is either invalid or full")

        new_state = copy.deepcopy(self)
        for i in range(self.rows):
            if new_state.board[col][i] == self.EMPTY:
                new_state.board[col][i] = new_state.next_player
                if new_state.check_winner(col, i):
                    new_state.winner = self.next_player

                new_state.next_player = self.flip_player[self.next_player]

                return new_state

    def check_winner(self, col, row):
        player = self.board[col, row]
        position = (col, row)
        original_c, original_r  = position[0], position[1]

        # vertical axis, horizontal axis, main diagonal, and secondary diagonal
        axes = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for i in range(len(axes)):
            axis = axes[i]
            neighbour_c, neighbour_r = original_c + axis[0], original_r + axis[1]
            total = 1

            while 0 <= neighbour_c < self.columns and 0 <= neighbour_r < self.rows and self.board[neighbour_c, neighbour_r] == player:
                total += 1
                neighbour_c, neighbour_r = neighbour_c + axis[0], neighbour_r + axis[1]

            # early return
            if total >= 3:
                return True

            neighbour_c, neighbour_r = original_c - axis[0], original_r - axis[1]

            while 0 <= neighbour_c < self.columns and 0 <= neighbour_r < self.rows and self.board[neighbour_c, neighbour_r] == player:
                total += 1
                neighbour_c, neighbour_r = neighbour_c - axis[0], neighbour_r - axis[1]

            if total >= 3:
                return True

        return False

class Minimax:
    def next_move(self):
        pass
    def get_value(self):
        pass

exemplo = ConnectN()
print (exemplo.board)
novo = exemplo.play(1)
print (novo.board)