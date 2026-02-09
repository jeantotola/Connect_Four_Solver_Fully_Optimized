import copy
import math
import numpy as np

class ConnectN:
    def __init__(self, rows=4, columns=5, win_condition=3):
        self.EMPTY = 0
        self.P1 = 1
        self.P2 = 2
        self.DRAW = 'DRAW'
        self.win_condition = win_condition

        self.winner = None

        self.rows = rows
        self.columns = columns

        self.next_player = self.P1
        self.flip_player = {self.P1: self.P2,self.P2: self.P1}

        self.board = np.zeros((self.columns, self.rows), dtype=int)

    def valid_move(self, col):
        return -1 < col < self.columns and self.board[col, self.rows - 1] == self.EMPTY

    def actions(self):
        # checks which columns have 0 at the top
        # np.where returns a tuple, the first element of which is made into a list with .tolist()
        return np.where(self.board[:, self.rows -1] == self.EMPTY)[0].tolist()

    def play(self, col):
        if not self.valid_move(col):
            raise ValueError("Column is either invalid or full")

        new_state = copy.deepcopy(self)

        for i in range(self.rows):
            if new_state.board[col][i] == self.EMPTY:
                new_state.board[col][i] = new_state.next_player

                new_state.winner = new_state.check_winner(col, i)

                new_state.next_player = self.flip_player[new_state.next_player]

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
            if total >= self.win_condition:
                return player

            neighbour_c, neighbour_r = original_c - axis[0], original_r - axis[1]

            while 0 <= neighbour_c < self.columns and 0 <= neighbour_r < self.rows and self.board[neighbour_c, neighbour_r] == player:
                total += 1
                neighbour_c, neighbour_r = neighbour_c - axis[0], neighbour_r - axis[1]

            if total >= self.win_condition:
                return player

        if not self.actions():
                return self.DRAW

        return None

class Minimax:
    def next_move(self, state = ConnectN()):
        player = state.next_player
        best_action = None
        best_value = -math.inf

        for action in state.actions():
            new_state = state.play(action)
            new_value = self.get_value(new_state, player, get_min = True)
            if new_value > best_value:
                best_value = new_value
                best_action = action

        return best_action

    def get_value(self, state, player, get_min, alpha = -math.inf, beta = math.inf):
        other_player = state.flip_player[player]
        winner = state.winner

        if winner == player:
            return 1
        if winner == other_player:
            return -1
        if winner == state.DRAW:
            return 0

        for action in state.actions():
            new_state = state.play(action)
            action_value = self.get_value(new_state, player, get_min = not get_min, alpha = alpha, beta = beta)

            if not get_min and action_value > alpha:
                alpha = action_value

            if get_min and action_value < beta:
                beta = action_value

            if alpha >= beta:
                return alpha if not get_min else beta
        return alpha if not get_min else beta


game = ConnectN()
ai = Minimax()

game = game.play(3)
move = ai.next_move(game)
game = game.play(move)

print (game.board)