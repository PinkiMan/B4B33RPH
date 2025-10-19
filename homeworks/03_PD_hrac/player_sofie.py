import random

class Sofie1:
    # DRUHY STRATEGIE: 
    '''Tit for Tat , Detective , Grim Trigger , Win-Stay-Lose-Shift, Pavlov , Adaptive'''

    # Instanci tridy MyPlayer lze vytvorit s 1 vstupnim parametrem (payoff matici) -> splneno
    # Instanci tridy MyPlayer lze vytvorit se 2 vstupnimi parametrami (payoff matici, pocet iteraci) -> splneno
    def __init__(self, payoff_matrix, number_of_iterations=None):
        self.payoff_matrix = payoff_matrix #((4,4), (1,6)), ((6,1), (2,2))
        self.number_of_iterations = number_of_iterations # dobre pro ruzne strategie, kde je potreba znat iterace
        self.my_moves = [] # uklada zde me tahy, abych se k nim pak mohla vracet
        self.opponent_moves = [] # uklada zde protihracovi tahy, abych se k nim pak mohla vracet
        # pro algoritmus Detective:
        self.test_sequence = [False, True, False, False]  # C, D, C, C
        self.turn = 0
        self.detected_defection = False     
        # pro algoritmus Grim Trigger:
        self.triggered = False

    def select_move(self):
        # VRACI TRUE NEBO FALSE
        strategy = 1 # nastavim druh me strategie


        #------------------------------------------------
        # strategie:Tit for Tat       (oko za oko)
        # -> kooperuje ale pokud souper podvede, tak ho kopiruje

        # První tah: kooperuji
        if not self.opponent_moves:
            return False
        # Jinak opakuje tah soupeře z minula
        return self.opponent_moves[-1]
        #------------------------------------------------


    # Metoda record_last_moves existuje a prijima muj a protihracum tah, resp. dva argumenty -> splneno
    def record_last_moves(self, my_last_move, opponent_last_move):
        self.my_moves.append(my_last_move)
        self.opponent_moves.append(opponent_last_move)
        # pro algoritmus Detective, zkoumam jestli me protihrac podvedl, pokud jo, tak menim strategii na tit for tat
        if opponent_last_move:
            self.detected_defection = True
        self.turn += 1
        # pro algoritmus Grim Trigger, chci vedet ze me protihrac podvedl
        if opponent_last_move:
            self.triggered = True


class Sofie2:
    # DRUHY STRATEGIE:
    '''Tit for Tat , Detective , Grim Trigger , Win-Stay-Lose-Shift, Pavlov , Adaptive'''

    # Instanci tridy MyPlayer lze vytvorit s 1 vstupnim parametrem (payoff matici) -> splneno
    # Instanci tridy MyPlayer lze vytvorit se 2 vstupnimi parametrami (payoff matici, pocet iteraci) -> splneno
    def __init__(self, payoff_matrix, number_of_iterations=None):
        self.payoff_matrix = payoff_matrix  # ((4,4), (1,6)), ((6,1), (2,2))
        self.number_of_iterations = number_of_iterations  # dobre pro ruzne strategie, kde je potreba znat iterace
        self.my_moves = []  # uklada zde me tahy, abych se k nim pak mohla vracet
        self.opponent_moves = []  # uklada zde protihracovi tahy, abych se k nim pak mohla vracet
        # pro algoritmus Detective:
        self.test_sequence = [False, True, False, False]  # C, D, C, C
        self.turn = 0
        self.detected_defection = False
        # pro algoritmus Grim Trigger:
        self.triggered = False

    def select_move(self):
        # VRACI TRUE NEBO FALSE
        strategy = 1  # nastavim druh me strategie

        # zkusi 4x otestovat souperovu kooperaci nebo podvody
        # dle toho se rozhodne jak dal
        if self.turn < len(self.test_sequence):
            move = self.test_sequence[self.turn]
        else:
            # pokud protihrac podvedl, tak zacne hrat titt for tat strategii
            if self.detected_defection:
                move = self.opponent_moves[-1]  # Tit for Tat
            else:
                move = True
        return move


    # Metoda record_last_moves existuje a prijima muj a protihracum tah, resp. dva argumenty -> splneno
    def record_last_moves(self, my_last_move, opponent_last_move):
        self.my_moves.append(my_last_move)
        self.opponent_moves.append(opponent_last_move)
        # pro algoritmus Detective, zkoumam jestli me protihrac podvedl, pokud jo, tak menim strategii na tit for tat
        if opponent_last_move:
            self.detected_defection = True
        self.turn += 1
        # pro algoritmus Grim Trigger, chci vedet ze me protihrac podvedl
        if opponent_last_move:
            self.triggered = True


class Sofie3:
    # DRUHY STRATEGIE:
    '''Tit for Tat , Detective , Grim Trigger , Win-Stay-Lose-Shift, Pavlov , Adaptive'''

    # Instanci tridy MyPlayer lze vytvorit s 1 vstupnim parametrem (payoff matici) -> splneno
    # Instanci tridy MyPlayer lze vytvorit se 2 vstupnimi parametrami (payoff matici, pocet iteraci) -> splneno
    def __init__(self, payoff_matrix, number_of_iterations=None):
        self.payoff_matrix = payoff_matrix  # ((4,4), (1,6)), ((6,1), (2,2))
        self.number_of_iterations = number_of_iterations  # dobre pro ruzne strategie, kde je potreba znat iterace
        self.my_moves = []  # uklada zde me tahy, abych se k nim pak mohla vracet
        self.opponent_moves = []  # uklada zde protihracovi tahy, abych se k nim pak mohla vracet
        # pro algoritmus Detective:
        self.test_sequence = [False, True, False, False]  # C, D, C, C
        self.turn = 0
        self.detected_defection = False
        # pro algoritmus Grim Trigger:
        self.triggered = False

    def select_move(self):
        # VRACI TRUE NEBO FALSE
        strategy = 1  # nastavim druh me strategie

        # ------------------------------------------------
        # strategie: Grim Trigger
        # -> zacne kooperovat ale jakmile souper podvede, tak podvadi taky

        # rozhodne se podle tahu soupere
        if self.triggered:
            return True  # DEFECT
        else:
            return False  # COOPERATE

    # Metoda record_last_moves existuje a prijima muj a protihracum tah, resp. dva argumenty -> splneno
    def record_last_moves(self, my_last_move, opponent_last_move):
        self.my_moves.append(my_last_move)
        self.opponent_moves.append(opponent_last_move)
        # pro algoritmus Detective, zkoumam jestli me protihrac podvedl, pokud jo, tak menim strategii na tit for tat
        if opponent_last_move:
            self.detected_defection = True
        self.turn += 1
        # pro algoritmus Grim Trigger, chci vedet ze me protihrac podvedl
        if opponent_last_move:
            self.triggered = True


class Sofie4:
    # DRUHY STRATEGIE:
    '''Tit for Tat , Detective , Grim Trigger , Win-Stay-Lose-Shift, Pavlov , Adaptive'''

    # Instanci tridy MyPlayer lze vytvorit s 1 vstupnim parametrem (payoff matici) -> splneno
    # Instanci tridy MyPlayer lze vytvorit se 2 vstupnimi parametrami (payoff matici, pocet iteraci) -> splneno
    def __init__(self, payoff_matrix, number_of_iterations=None):
        self.payoff_matrix = payoff_matrix  # ((4,4), (1,6)), ((6,1), (2,2))
        self.number_of_iterations = number_of_iterations  # dobre pro ruzne strategie, kde je potreba znat iterace
        self.my_moves = []  # uklada zde me tahy, abych se k nim pak mohla vracet
        self.opponent_moves = []  # uklada zde protihracovi tahy, abych se k nim pak mohla vracet
        # pro algoritmus Detective:
        self.test_sequence = [False, True, False, False]  # C, D, C, C
        self.turn = 0
        self.detected_defection = False
        # pro algoritmus Grim Trigger:
        self.triggered = False

    def select_move(self):
        # VRACI TRUE NEBO FALSE
        strategy = 1  # nastavim druh me strategie

        # ------------------------------------------------
        # strategie: Win-Stay-Lose-Shift
        # -> zkouma jestli jeho predesly tah byl uspesny a pokud jo, tak ho opakuje

        # zacina kooperaci jako prvni tah
        if not self.my_moves:
            return False

        last_my = self.my_moves[-1]
        last_op = self.opponent_moves[-1]
        reward = self.payoff_matrix[last_my][last_op][0]

        # pokud zisk >= 3, opakuje tah, tzn. pokud vysel podvod nebo kooperace, tak pokracuje
        if reward >= 3:
            return last_my
        else:
            # pokud se nepovedlo, tak meni strategii
            return not last_my


    # Metoda record_last_moves existuje a prijima muj a protihracum tah, resp. dva argumenty -> splneno
    def record_last_moves(self, my_last_move, opponent_last_move):
        self.my_moves.append(my_last_move)
        self.opponent_moves.append(opponent_last_move)
        # pro algoritmus Detective, zkoumam jestli me protihrac podvedl, pokud jo, tak menim strategii na tit for tat
        if opponent_last_move:
            self.detected_defection = True
        self.turn += 1
        # pro algoritmus Grim Trigger, chci vedet ze me protihrac podvedl
        if opponent_last_move:
            self.triggered = True


class Sofie5:
    # DRUHY STRATEGIE:
    '''Tit for Tat , Detective , Grim Trigger , Win-Stay-Lose-Shift, Pavlov , Adaptive'''

    # Instanci tridy MyPlayer lze vytvorit s 1 vstupnim parametrem (payoff matici) -> splneno
    # Instanci tridy MyPlayer lze vytvorit se 2 vstupnimi parametrami (payoff matici, pocet iteraci) -> splneno
    def __init__(self, payoff_matrix, number_of_iterations=None):
        self.payoff_matrix = payoff_matrix  # ((4,4), (1,6)), ((6,1), (2,2))
        self.number_of_iterations = number_of_iterations  # dobre pro ruzne strategie, kde je potreba znat iterace
        self.my_moves = []  # uklada zde me tahy, abych se k nim pak mohla vracet
        self.opponent_moves = []  # uklada zde protihracovi tahy, abych se k nim pak mohla vracet
        # pro algoritmus Detective:
        self.test_sequence = [False, True, False, False]  # C, D, C, C
        self.turn = 0
        self.detected_defection = False
        # pro algoritmus Grim Trigger:
        self.triggered = False

    def select_move(self):
        # VRACI TRUE NEBO FALSE
        strategy = 1  # nastavim druh me strategie

        # ------------------------------------------------
        # strategie: Pavlov
        # -> pokud souper spolupracuje pokud jsme se oba shodli na tahu, ale jinak menime strategii

        # zacina kooperaci jako prvni tah
        if not self.my_moves:
            return False

            # pokud jsme se shodli na tahu, tak pokracuju
        if self.my_moves[-1] == self.opponent_moves[-1]:
            return self.my_moves[-1]
        else:
            # pokud jsme se neshodli, tak menim strategii
            return not self.my_moves[-1]


    # Metoda record_last_moves existuje a prijima muj a protihracum tah, resp. dva argumenty -> splneno
    def record_last_moves(self, my_last_move, opponent_last_move):
        self.my_moves.append(my_last_move)
        self.opponent_moves.append(opponent_last_move)
        # pro algoritmus Detective, zkoumam jestli me protihrac podvedl, pokud jo, tak menim strategii na tit for tat
        if opponent_last_move:
            self.detected_defection = True
        self.turn += 1
        # pro algoritmus Grim Trigger, chci vedet ze me protihrac podvedl
        if opponent_last_move:
            self.triggered = True


class Sofie6:
    # DRUHY STRATEGIE:
    '''Tit for Tat , Detective , Grim Trigger , Win-Stay-Lose-Shift, Pavlov , Adaptive'''

    # Instanci tridy MyPlayer lze vytvorit s 1 vstupnim parametrem (payoff matici) -> splneno
    # Instanci tridy MyPlayer lze vytvorit se 2 vstupnimi parametrami (payoff matici, pocet iteraci) -> splneno
    def __init__(self, payoff_matrix, number_of_iterations=None):
        self.payoff_matrix = payoff_matrix  # ((4,4), (1,6)), ((6,1), (2,2))
        self.number_of_iterations = number_of_iterations  # dobre pro ruzne strategie, kde je potreba znat iterace
        self.my_moves = []  # uklada zde me tahy, abych se k nim pak mohla vracet
        self.opponent_moves = []  # uklada zde protihracovi tahy, abych se k nim pak mohla vracet
        # pro algoritmus Detective:
        self.test_sequence = [False, True, False, False]  # C, D, C, C
        self.turn = 0
        self.detected_defection = False
        # pro algoritmus Grim Trigger:
        self.triggered = False

    def select_move(self):
        # VRACI TRUE NEBO FALSE
        strategy = 1  # nastavim druh me strategie


        # ------------------------------------------------
        # strategie: Adaptive
        # -> adaptuju se souperove strategii a zkoumam jeho posledni tahy, podle toho pak menim moje

        # zacina kooperaci jako prvni tah
        if not self.opponent_moves:
            return False

            # vypocitam jak casto me protihrac podvadi
        defect_rate = sum(self.opponent_moves) / len(self.opponent_moves)

        # pokud me podvadi mene nez 40%, tak kooperuju
        return defect_rate > 0.4
        # ------------------------------------------------

    # Metoda record_last_moves existuje a prijima muj a protihracum tah, resp. dva argumenty -> splneno
    def record_last_moves(self, my_last_move, opponent_last_move):
        self.my_moves.append(my_last_move)
        self.opponent_moves.append(opponent_last_move)
        # pro algoritmus Detective, zkoumam jestli me protihrac podvedl, pokud jo, tak menim strategii na tit for tat
        if opponent_last_move:
            self.detected_defection = True
        self.turn += 1
        # pro algoritmus Grim Trigger, chci vedet ze me protihrac podvedl
        if opponent_last_move:
            self.triggered = True