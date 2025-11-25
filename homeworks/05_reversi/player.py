__author__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__date__ = "09/11/2025"

"""
Project: B4B33RPH
Filename: player.py
Directory: homeworks/05_reversi/
"""

import random

POSITION_WEIGHTS = [
    [1000, -200, 50, 50, 50, 50, -200, 1000],
    [-200, -300, -10, -10, -10, -10, -300, -200],
    [50, -10,  5,  1,  1,  5, -10, 50],
    [50, -10,  1,  0,  0,  1, -10, 50],
    [50, -10,  1,  0,  0,  1, -10, 50],
    [50, -10,  5,  1,  1,  5, -10, 50],
    [-200, -300, -10, -10, -10, -10, -300, -200],
    [1000, -200, 50, 50, 50, 50, -200, 1000],
]


def get_all_empty_moves(board):
    empty_moves = []

    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == -1:
                empty_moves.append((y, x))

    return empty_moves



class MyPlayer:
    """ Plays valid move """

    def __init__(self, my_color, opponent_color):
        self.my_color = my_color
        self.opponent_color = opponent_color

    def select_move(self, board):
        valid_moves = self._get_all_valid_moves(board)
        if len(valid_moves) == 0:
            return None

        best_move = valid_moves[0]
        best_score = self.score_move(best_move)

        for move in valid_moves:
            score = self.score_move(move)
            if score > best_score:
                best_move = move
                best_score = score

        return best_move


    def _is_correct_move(self, move, board):
        dys = [-1, -1, -1, 0, 0, 1, 1, 1]
        dxs = [-1, 0, 1, -1, 1, -1, 0, 1]

        for dy, dx in zip(dys, dxs):
            if 0<=move[1]+dx<len(board) and 0<=move[0]+dy<len(board):
                if board[move[0]+dy][move[1]+dx] == self.opponent_color:
                    if self._direction_test(board, dx,dy,move):
                        return True
        return False

    def _direction_test(self, board, dx, dy, move):
        position = [move[0], move[1]]

        while True:
            position[0] += dy
            position[1] += dx

            if 0<=position[0]<len(board) and 0<=position[1]<len(board):
                if board[position[0]][position[1]] == self.opponent_color:
                    pass
                elif board[position[0]][position[1]] == self.my_color:
                    return True
                else:
                    return False
            else:
                return False


    def _get_all_valid_moves(self, board) -> list:
        valid_moves = []

        empty_moves = get_all_empty_moves(board=board)

        for move in empty_moves:
            if self._is_correct_move(move, board):
                if move not in valid_moves:
                    valid_moves.append(move)

        return valid_moves

    def _get_all_valid_moves_color(self, board, color) -> list:
        old_my_color = self.my_color
        old_opponent_color = self.opponent_color

        self.my_color = color
        self.opponent_color = old_my_color if color == old_opponent_color else old_opponent_color

        valid_moves = self._get_all_valid_moves(board)

        self.my_color = old_my_color
        self.opponent_color = old_opponent_color

        return valid_moves

    def score_move(self, move):
        score = POSITION_WEIGHTS[move[0]][move[1]]
        return score

    def evaluate(self, board):
        score = 0


if __name__ == '__main__':
    mp = MyPlayer(0,1)
    pole = [[0,1,0,0,0,0,0,0],
            [-1,0,1,0,0,0,0,0],
            [1,0,1,1,1,0,0,0],
            [1,0,0,1,0,0,0,0],
            [1,0,0,0,0,0,0,0],
            [1,-1,0,0,0,0,0,0],
            [1,1,0,1,1,0,0,0],
            [0,0,0,0,0,0,0,0,]]

    print(mp.select_move(pole))
