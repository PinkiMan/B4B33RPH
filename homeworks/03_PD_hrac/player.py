__author__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__date__ = "30/09/2025"

"""
Project: B4B33RPH
Filename: player.py
Directory: homeworks/03_PD_hrac/
"""

import random
import unittest

# TODO: add detection for tournament against my self

"""
    2p - 

"""

class MyPlayer:
    """ Play best point combination move """
    def __init__(self, payoff_matrix: list, number_of_iterations: int = None) -> None:
        self.payoff_matrix = payoff_matrix
        if number_of_iterations is not None:
            self.number_of_iterations = number_of_iterations
        else:
            self.number_of_iterations = 100

        self.handshake = [1, 0, 1, 1, 0, 1, 0, 0]
        self.rounds_played = 0

        self.history = []

        self.it_is_me = False

    def select_move(self) -> bool:
        if self.payoff_matrix[0][0][0] + self.payoff_matrix[0][1][0] > self.payoff_matrix[1][0][0] + \
                self.payoff_matrix[1][1][0]:
            return False
        else:
            return True

        """if self.rounds_played < len(self.handshake):
            return True if self.handshake[self.rounds_played]==1 else False

        elif self.it_is_me and self.rounds_played > len(self.handshake):
            if self.payoff_matrix[0][0][0] + self.payoff_matrix[0][0][1] > self.payoff_matrix[1][1][0] + self.payoff_matrix[1][1][1]:
                return False
            else:
                return True

        else:
            if self.payoff_matrix[0][0][0] + self.payoff_matrix[0][1][0] > self.payoff_matrix[1][0][0] + self.payoff_matrix[1][1][0]:
                return False
            else:
                return True"""

    def is_it_me(self):
        for i, (my_turn, enemy_turn) in enumerate(self.history):
            if my_turn != enemy_turn != self.handshake[i]:
                return False
        return True

    def record_last_moves(self, my_last_move, opponent_last_move) -> None:
        self.history.append((my_last_move, opponent_last_move))
        self.rounds_played += 1

        if self.rounds_played == len(self.handshake):
            self.it_is_me = self.is_it_me()
            if self.it_is_me:
                #print("it is me")
                pass


if __name__ == '__main__':
    pass
