__author__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__date__ = "09/11/2025"

"""
Project: B4B33RPH
Filename: player.py
Directory: homeworks/05_reversi/
"""

import copy

POSITION_WEIGHTS = [
    [2000, -200, 50, 50, 50, 50, -200, 2000],
    [-200, -300, -10, -10, -10, -10, -300, -200],
    [50, -10, 5, 1, 1, 5, -10, 50],
    [50, -10, 1, 0, 0, 1, -10, 50],
    [50, -10, 1, 0, 0, 1, -10, 50],
    [50, -10, 5, 1, 1, 5, -10, 50],
    [-200, -300, -10, -10, -10, -10, -300, -200],
    [2000, -200, 50, 50, 50, 50, -200, 2000],
]

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1), (0, 1),
              (1, -1), (1, 0), (1, 1)]


class MyPlayer:
    """ Plays valid move """

    def __init__(self, my_color, opponent_color):
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.cache = {}  # dict of all calculated moves for reuse

    def select_move(self, board):
        """
        :param board: n*n matrix of actual state of game board
        :return: (row, column) coordination of my move
        """

        valid_moves = self._get_all_valid_moves_color(board, self.my_color)  # gets all valid moves
        if len(valid_moves) == 0:  # if no valid point dont play
            return None

        empty = len(self.__get_all_empty_moves(board))  # gets number of empty points

        if empty <= 24:
            depth = 2
        elif empty <= 18:
            depth = 4
        elif empty <= 12:
            depth = 6
        elif empty <= 10:
            depth = 8
        else:
            depth = 2

        best_move = None
        best_score = -float('inf')

        for move in valid_moves:  # finds best move with minimax
            new_board = self.__simulate_move(board, move, self.my_color)  # create board with move applied
            score = self._minimax(new_board, depth - 1, -float('inf'), float('inf'), False)  # run minimax

            if score > best_score:  # if move has more score than best move set to best move
                best_move = move
                best_score = score

        return best_move

    def __direction_test(self, board, dx, dy, move) -> bool:
        """
        :param board: n*n matrix of actual state of game board
        :param dx: x direction
        :param dy: y direction
        :param move: move to make in board
        :return: checks if move has valid ending in direction
        """
        position = [move[0], move[1]]  # move position

        while True:
            position[0] += dy
            position[1] += dx

            if 0 <= position[0] < len(board) and 0 <= position[1] < len(board):  # check if position is on board
                if board[position[0]][position[1]] == self.opponent_color:  # if opponent color continue
                    pass
                elif board[position[0]][position[1]] == self.my_color:  # if my color then it is valid
                    return True
                else:
                    return False
            else:
                return False

    def __is_correct_move(self, move, board) -> bool:
        """
        :param move: move to make in board
        :param board: n*n matrix of actual state of game board
        :return: validation if move is valid
        """
        for dy, dx in DIRECTIONS:  # cycles through all directions around move
            ny, nx = move[0] + dy, move[1] + dx  # applies move to point
            if 0 <= nx < len(board) and 0 <= ny < len(board):  # checks if nx,ny are on board
                if board[ny][nx] == self.opponent_color:  # checks if point is opponent's
                    if self.__direction_test(board, dx, dy, move):  # checks if at the end is my color point
                        return True  # move is valid
        return False  # move is not valid

    @staticmethod
    def __get_all_empty_moves(board) -> list:
        """
        :param board: n*n matrix of actual state of game board
        :return: all empty moves on board
        """
        empty_moves = []

        for y in range(len(board)):  # cycles thought board and finds empty slots
            for x in range(len(board)):
                if board[y][x] == -1:  # checks if point is empty
                    empty_moves.append((y, x))

        return empty_moves

    def __get_all_valid_moves(self, board) -> list:
        """
        :param board: n*n matrix of actual state of game board
        :return: all valid moves on board with my color
        """
        valid_moves = []

        empty_moves = self.__get_all_empty_moves(board=board)  # all empty moves

        for move in empty_moves:  # cycles through all empty moves and find valid ones
            if self.__is_correct_move(move, board):  # checks if move is valid
                if move not in valid_moves:  # adds move to valid moves if it is not there already
                    valid_moves.append(move)

        return valid_moves

    def _get_all_valid_moves_color(self, board, color) -> list:
        """
        :param board: n*n matrix of actual state of game board
        :param color: color of plyer playing
        :return: all valid moves on board with color
        """
        # saves default colors
        old_my_color = self.my_color
        old_opponent_color = self.opponent_color

        # swaps default colors if needed
        self.my_color = color
        self.opponent_color = old_my_color if color == old_opponent_color else old_opponent_color

        valid_moves = self.__get_all_valid_moves(board)  # gets all valid moves for actual my color

        # sets colors to original color
        self.my_color = old_my_color
        self.opponent_color = old_opponent_color

        return valid_moves

    def _evaluate_board(self, board) -> float:
        """
        :param board: n*n matrix of actual state of game board
        :return: score of board
        """
        score = 0

        my_moves = len(self._get_all_valid_moves_color(board=board, color=self.my_color))
        opponent_moves = len(self._get_all_valid_moves_color(board=board, color=self.opponent_color))

        if my_moves + opponent_moves == 0:
            piece_diff = 0
        else:
            piece_diff = 10 * (my_moves - opponent_moves) / (my_moves + opponent_moves)
        score += piece_diff

        my_count = 0
        opponent_count = 0

        for y in range(len(board)):
            for x in range(len(board)):
                if board[y][x] == self.my_color:
                    score += POSITION_WEIGHTS[y][x]
                    my_count += 1
                elif board[y][x] == self.opponent_color:
                    score -= POSITION_WEIGHTS[y][x]
                    opponent_count += 1

        # TODO: add corner penalty and count corner ownership

        return score

    def __simulate_move(self, board, move, color) -> tuple:
        """
        :param board: n*n matrix of actual state of game board
        :param move: move to make in board
        :param color: color of plyer playing
        :return: board after move
        """
        new_board = copy.deepcopy(board)  # creates copy of actual board
        flips = self.__get_flips(board=board, move=move, color=color)  # gets all flips for actual board and move

        if len(flips) == 0:  # returns copy of board if move don't change anything
            return new_board

        new_board[move[0]][move[1]] = color  # sets point on board by move with color

        for (fy, fx) in flips:  # sets all flips to board with color
            new_board[fy][fx] = color

        return new_board

    def __get_flips(self, board, move, color) -> list:
        """
        :param board: n*n matrix of actual state of game board
        :param move: move to make in board
        :param color: color of plyer playing
        :return: all flipped locations on actual board
        """
        opponent_color = self.opponent_color if color == self.my_color else self.my_color  # color of opponent

        flips = []

        for dy, dx in DIRECTIONS:  # cycles through directions
            path = []

            ny, nx = move[0] + dy, move[1] + dx  # moves point with direction

            while 0 <= ny < len(board) and 0 <= nx < len(board) and board[ny][nx] == opponent_color:  # checks if on board
                path.append((ny, nx))
                ny += dy
                nx += dx
            if 0 <= ny < len(board) and 0 <= nx < len(board) and board[ny][nx] == color and len(path) != 0:  # adds path of flips to flips
                flips.extend(path)
        return flips

    @staticmethod
    def __board_to_key(board) -> tuple[tuple, ...]:
        """
        :param board: n*n matrix of actual state of game board
        :return: key of board representing actual state of game board
        """
        return tuple(tuple(row) for row in board)

    def _minimax(self, board, depth, alpha, beta, maximizing):
        """
        :param board: n*n matrix of actual state of game board
        :param depth: depth for finding moves
        :param alpha: best max score
        :param beta: best min score
        :param maximizing: if maximize or minimize score
        :return: score of board on depth
        """
        key = (self.__board_to_key(board), depth, maximizing)  # gets key of each

        if key in self.cache:  # returns existing value instead calculating again
            return self.cache[key]

        # gets valid moves for my color and opponent's
        valid_my = self._get_all_valid_moves_color(board, self.my_color)
        valid_opp = self._get_all_valid_moves_color(board, self.opponent_color)

        if depth == 0 or (not valid_my and not valid_opp):  # if depth == 0 evaluate board
            val = self._evaluate_board(board)
            self.cache[key] = val
            return val

        if maximizing:  # if maximizing get max score
            value = -float('inf')
            moves = valid_my
            if len(moves) == 0:  # if no moves
                value = max(value, self._minimax(board, depth - 1, alpha, beta, False))
            else:
                for move in moves:
                    new_board = self.__simulate_move(board, move, self.my_color)  # simulate move on board
                    value = max(value, self._minimax(new_board, depth - 1, alpha, beta, False))  # gets max score
                    alpha = max(alpha, value)  # sets alfa
                    if alpha >= beta:  # alfa beta break
                        break
            self.cache[key] = value  # add to cache
            return value
        else:  # get min score
            value = float('inf')
            moves = valid_opp
            if len(moves) == 0:  # if no moves
                value = min(value, self._minimax(board, depth - 1, alpha, beta, True))
            else:
                for move in moves:
                    new_board = self.__simulate_move(board, move, self.opponent_color)  # simulate move on board
                    value = min(value, self._minimax(new_board, depth - 1, alpha, beta, True))  # gets min score
                    beta = min(beta, value)  # sets beta
                    if beta <= alpha:  # alfa beta break
                        break
            self.cache[key] = value  # add to cache
            return value


if __name__ == '__main__':
    mp = MyPlayer(0, 1)
    pole = [[0, 1, 0, 0, 0, 0, 0, 0],
            [-1, 0, 1, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, -1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, ]]
    val = mp._get_all_valid_moves_color(pole, 0)
    print(val)

    # print(mp.select_move(pole))