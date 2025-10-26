__author__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__date__ = "30/09/2025"

"""
Project: B4B33RPH
Filename: player.py
Directory: homeworks/03_PD_hrac/
"""

# TODO: add better moves for game against self

""" SPECIFICATIONS:
  [x] filename is player.py
  [x] docstring not empty
  [x] 1 or 2 arguments on creation
  [x] select_move returns bool
  [x] record_last_moves accepts two arguments
"""

DEFECT = True   # 1
COOPERATE = False   # 0

class MyPlayer:
    """ Identify self or play best move """

    def __init__(self, payoff_matrix: list, number_of_iterations: int = None) -> None:
        self.payoff_matrix = payoff_matrix
        self.number_of_iterations = number_of_iterations
        self.history = []  # history of moves played by both players

        self.__handshake = [1, 0, 1, 1, 0, 1, 0, 0]  # random moves always played at start for handshake teammate
        self.__rounds_played = 0  # already played rounds
        self.it_is_me = False  # checked if playing against self

        self.__best_decision_move = self.select_move()  # best move against unknown players

    def __best_decision(self) -> bool:
        """ Returns best move based on payoff matrix (tested against 16 basic strategies) """
        if self.payoff_matrix[0][0][0] + self.payoff_matrix[0][1][0] > self.payoff_matrix[1][0][0] + \
                self.payoff_matrix[1][1][0]:
            return False
        else:
            return True

    def select_move(self) -> bool:
        """ Select the best move """
        if self.__rounds_played < len(self.__handshake):  # play handshake
            return DEFECT if self.__handshake[self.__rounds_played] == 1 else COOPERATE

        elif self.it_is_me and self.__rounds_played > len(self.__handshake):  # play against self
            if self.payoff_matrix[0][0][0] + self.payoff_matrix[0][0][1] > self.payoff_matrix[1][1][0] + \
                    self.payoff_matrix[1][1][1]:
                return False
            else:
                return True
        else:  # play against unknown enemy
            return self.__best_decision_move

    def __is_it_me(self):
        """ Check if playing against self """
        for i, (my_turn, enemy_turn) in enumerate(self.history):  # test last n moves was same as mine and handshake
            if my_turn != enemy_turn != self.__handshake[i]:
                return False  # not playing self
        return True  # playing against self

    def record_last_moves(self, my_last_move, opponent_last_move) -> None:
        """ Record last moves played by both players """
        self.history.append((my_last_move, opponent_last_move))  # add moves to history
        self.__rounds_played += 1  # count round

        if self.__rounds_played == len(self.__handshake):
            self.it_is_me = self.__is_it_me()


if __name__ == '__main__':
    pass
