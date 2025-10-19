import unittest


class TestPlayer(unittest.TestCase):
    def set_up(self):
        random_number_a = random.randrange(0, 100)
        random_number_b = random.randrange(0, 100)
        random_number_c = random.randrange(0, 100)
        random_number_d = random.randrange(0, 100)
        self.payoff_matrix = [[(random_number_a, random_number_a), (random_number_b, random_number_c)],
                         [(random_number_c, random_number_b), (random_number_d, random_number_d)]]

        self.rounds = random.randrange(0, 100)

    def init_test_1(self):
        player = MyPlayer(payoff_matrix=self.payoff_matrix)
        self.assertEqual(player.payoff_matrix, self.payoff_matrix)
        self.assertEqual(player.history, [])

    def init_test_2(self):
        player = MyPlayer(payoff_matrix=self.payoff_matrix, number_of_iterations=self.rounds)
        self.assertEqual(player.payoff_matrix, self.payoff_matrix)
        self.assertEqual(player.history, [])
        self.assertEqual(player.number_of_iterations, self.rounds)

    def test_record_last_moves(self):
        player = MyPlayer(self.payoff_matrix)
        player.record_last_moves(True, False)
        self.assertEqual(player.history, [(True, False)])

    def test_handshake_moves(self):
        player = MyPlayer(self.payoff_matrix)
        handshake = [1, 0, 1, 1, 0, 1, 0, 0]
        for expected in handshake:
            move = player.select_move()
            self.assertEqual(move, bool(expected))
            player.record_last_moves(move, move)

if __name__ == '__main__':
    unittest.main()
