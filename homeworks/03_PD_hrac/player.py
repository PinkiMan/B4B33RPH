__author__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__date__ = "30/09/2025"

import random

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

""" STRATEGY:
 1. against unknown player:
    a. play coop if moves with my coop has more points than if with defect
        [[(4, 4), (1, 6)], [(6, 1), (2, 2)]] => 4+1 < 6+2 => defect
 2. against self:
    a. play coop if 2*coop is most points
    b. play defect if 2*defect is most points
    c. play combination of coop and defect simultaneously
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
        self.__it_is_me = False  # checked if playing against self

        self.__both_coop = False
        self.__both_defect = False
        self.__different_play = False

        self.__my_different_play = None

        self.__best_decision_move = self.select_move()  # best move against unknown players

    def __best_decision(self) -> bool:
        """ Returns best move based on payoff matrix (tested against 16 basic strategies) """
        if self.payoff_matrix[0][0][0] + self.payoff_matrix[0][1][0] > self.payoff_matrix[1][0][0] + \
                self.payoff_matrix[1][1][0]:
            return COOPERATE
        else:
            return DEFECT

    def select_move(self) -> bool:
        """ Select the best move """
        if self.__rounds_played < len(self.__handshake):  # play handshake
            return DEFECT if self.__handshake[self.__rounds_played] == 1 else COOPERATE

        elif self.__it_is_me and self.__rounds_played > len(self.__handshake):  # play against self
            if self.__both_coop:
                return COOPERATE
            elif self.__both_defect:
                return DEFECT
            elif self.__different_play:
                if self.__my_different_play is None:
                    return random.choice([COOPERATE, DEFECT])
                else:
                    return DEFECT if self.__my_different_play == 1 else COOPERATE
            else:
                return COOPERATE

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
            self.__it_is_me = self.__is_it_me()

            if self.__it_is_me:
                both_coop = self.payoff_matrix[COOPERATE][COOPERATE][0] + self.payoff_matrix[COOPERATE][COOPERATE][1]
                both_defect = self.payoff_matrix[DEFECT][DEFECT][0] + self.payoff_matrix[DEFECT][DEFECT][1]
                different_play = self.payoff_matrix[COOPERATE][DEFECT][0] + self.payoff_matrix[COOPERATE][DEFECT][1]

                if both_coop > different_play and both_coop > both_defect:  # both coop
                    self.__both_coop = True
                elif both_defect > different_play and both_defect > both_coop:  # both defect
                    self.__both_defect = True
                elif different_play > both_defect and different_play > both_coop:   # one coop second defect
                    self.__different_play = True
                else:   # fallback to both coop
                    self.__both_coop = True

        elif self.__rounds_played > len(self.__handshake) and self.__different_play and self.__my_different_play is None: # save move for self play diff
            if my_last_move != opponent_last_move:
                self.__my_different_play = my_last_move


if __name__ == '__main__':
    pass
