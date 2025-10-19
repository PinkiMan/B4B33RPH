import random


class MyPlayer:
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
        # pro algoritmus TFT Spiteful:
        self.spite_triggered = False
        # pro algoritmus ORE:
        self.total_reward_C = 0
        self.count_C = 0
        self.total_reward_D = 0
        self.count_D = 0
        # pro algoritmus GTFT:
        self.strategy = "GTFT"
        # pro algoritmus Adaptivni GTFT:
        self.noise_counter = 0
        self.R = payoff_matrix[0][0][0]
        self.P = payoff_matrix[1][1][0]
        self.T = payoff_matrix[1][0][0]
        self.S = payoff_matrix[0][1][0]
        self.g = min(1 - (self.T - self.R) / (self.R - self.S), (self.R - self.P) / (self.T - self.P))

    def select_move(self):
        # VRACI TRUE NEBO FALSE
        strategy = 1  # nastavim druh me strategie

        # ------------------------------------------------
        # strategie:Tit for Tat       (oko za oko)
        # -> kooperuje ale pokud souper podvede, tak ho kopiruje

        if strategy == 1:
            # První tah: kooperuji
            if not self.opponent_moves:
                return False
            # Jinak opakuje tah soupeře z minula
            return self.opponent_moves[-1]
        # ------------------------------------------------
        # strategie: Detective
        # -> testuje souperovu loajalitu a pokud podvede, tak zacne hrat oko za oko

        if strategy == 2:
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
        # ------------------------------------------------
        # strategie: Grim Trigger
        # -> zacne kooperovat ale jakmile souper podvede, tak podvadi taky

        if strategy == 3:
            # rozhodne se podle tahu soupere
            if self.triggered:
                return True  # DEFECT
            else:
                return False  # COOPERATE
        # ------------------------------------------------
        # strategie: Win-Stay-Lose-Shift
        # -> zkouma jestli jeho predesly tah byl uspesny a pokud jo, tak ho opakuje

        if strategy == 4:
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
        # ------------------------------------------------
        # strategie: Pavlov
        # -> pokud souper spolupracuje pokud jsme se oba shodli na tahu, ale jinak menime strategii

        if strategy == 5:
            # zacina kooperaci jako prvni tah
            if not self.my_moves:
                return False

            # pokud jsme se shodli na tahu, tak pokracuju
            if self.my_moves[-1] == self.opponent_moves[-1]:
                return self.my_moves[-1]
            else:
                # pokud jsme se neshodli, tak menim strategii
                return not self.my_moves[-1]
        # ------------------------------------------------
        # strategie: Adaptive
        # -> adaptuju se souperove strategii a zkoumam jeho posledni tahy, podle toho pak menim moje

        if strategy == 6:
            # zacina kooperaci jako prvni tah
            if not self.opponent_moves:
                return False

            # vypocitam jak casto me protihrac podvadi
            defect_rate = sum(self.opponent_moves) / len(self.opponent_moves)

            # pokud me podvadi mene nez 40%, tak kooperuju
            return defect_rate > 0.4
        # ------------------------------------------------
        # strategie: TFT Spiteful
        # -> hraje oko za oko ale po podvodu uz nespolupracuje

        if strategy == 7:
            # rozhodne se podle tahu soupere
            if self.spite_triggered:
                return True
            # zacina kooperaci jako prvni tah
            if not self.opponent_moves:
                return False

            return self.opponent_moves[-1]  # Tit for Tat
        # ------------------------------------------------
        # strategie: ORE
        # -> adpatuje se podle vahy C nebo D

        if strategy == 8:
            # zacne kooperovat
            if self.count_C == 0 and self.count_D == 0:
                return False
            avg_C = self.total_reward_C / self.count_C if self.count_C > 0 else 0
            avg_D = self.total_reward_D / self.count_D if self.count_D > 0 else 0
            return avg_D > avg_C  # vybere tah s vyssim prumernym ziskem
        # ------------------------------------------------
        # strategie: GTFT
        # ->

        if strategy == 9:
            if self.strategy == "GRIM" and self.triggered:
                return True  # DEFECT navždy

            if self.turn < 6:
                # GTFT fáze
                if self.turn == 0:
                    return False  # první tah: COOPERATE
                if self.opponent_moves[-1]:
                    # po zradě spolupracuje s pravděpodobností g(R,P,T,S)
                    R = self.payoff_matrix[0][0][0]
                    P = self.payoff_matrix[1][1][0]
                    T = self.payoff_matrix[1][0][0]
                    S = self.payoff_matrix[0][1][0]
                    g = min(1 - (T - R) / (R - S), (R - P) / (T - P))
                    return random.random() < max(0, min(1, g))
                else:
                    return False  # opakuje spolupráci
            else:
                # Po 6. kole: adaptivní rozhodnutí
                defect_rate = sum(self.opponent_moves) / len(self.opponent_moves)
                if defect_rate > 0.6:
                    self.strategy = "GRIM"
                    self.triggered = True
                    return True
                elif defect_rate > 0.3:
                    self.strategy = "PAVLOV"
                    if self.my_moves[-1] == self.opponent_moves[-1]:
                        return self.my_moves[-1]
                    else:
                        return not self.my_moves[-1]
                else:
                    self.strategy = "GTFT"
                    if self.opponent_moves[-1]:
                        R = self.payoff_matrix[0][0][0]
                        P = self.payoff_matrix[1][1][0]
                        T = self.payoff_matrix[1][0][0]
                        S = self.payoff_matrix[0][1][0]
                        g = min(1 - (T - R) / (R - S), (R - P) / (T - P))
                        return random.random() < max(0, min(1, g))
                    else:
                        return False
        # ------------------------------------------------
        # strategie: Adaptivni GTFT
        # ->

        if strategy == 10:

            if self.strategy == "GRIM" and self.triggered:
                return True  # DEFECT navždy

            if self.turn < 6:
                # GTFT fáze
                if self.turn == 0:
                    return False  # první tah: COOPERATE
                if self.opponent_moves[-1]:
                    return random.random() < max(0, min(1, self.g))
                else:
                    return False
            else:
                # Detekce šumu: pokud hráč spolupracoval a soupeř podvedl
                if self.my_moves[-1] == False and self.opponent_moves[-1] == True:
                    self.noise_counter += 1

                # Přepnutí strategie podle chování soupeře
                defect_rate = sum(self.opponent_moves) / len(self.opponent_moves)
                if defect_rate > 0.6 and self.noise_counter < 2:
                    self.strategy = "GRIM"
                    self.triggered = True
                    return True
                elif defect_rate > 0.3:
                    self.strategy = "PAVLOV"
                    if self.my_moves[-1] == self.opponent_moves[-1]:
                        return self.my_moves[-1]
                    else:
                        return not self.my_moves[-1]
                else:
                    self.strategy = "GTFT"
                    if self.opponent_moves[-1]:
                        return random.random() < max(0, min(1, self.g))
                    else:
                        return False
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
        # pro algoritmus TFT Spiteful, chci vedet ze me protihrac podvedl
        if opponent_last_move:
            self.spite_triggered = True
        # pro algorimus ORE
        reward = self.payoff_matrix[my_last_move][opponent_last_move][0]
        if my_last_move:
            self.total_reward_D += reward
            self.count_D += 1
        else:
            self.total_reward_C += reward
            self.count_C += 1
        # pro algoritmus GTFT
        if self.strategy == "GRIM" and opponent_last_move:
            self.triggered = True


import random


class Sofie7:
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
        # pro algoritmus TFT Spiteful:
        self.spite_triggered = False
        # pro algoritmus ORE:
        self.total_reward_C = 0
        self.count_C = 0
        self.total_reward_D = 0
        self.count_D = 0
        # pro algoritmus GTFT:
        self.strategy = "GTFT"
        # pro algoritmus Adaptivni GTFT:
        self.noise_counter = 0
        self.R = payoff_matrix[0][0][0]
        self.P = payoff_matrix[1][1][0]
        self.T = payoff_matrix[1][0][0]
        self.S = payoff_matrix[0][1][0]
        self.g = min(1 - (self.T - self.R) / (self.R - self.S), (self.R - self.P) / (self.T - self.P))

    def select_move(self):
        # VRACI TRUE NEBO FALSE
        strategy = 1  # nastavim druh me strategie

        # ------------------------------------------------
        # strategie: TFT Spiteful
        # -> hraje oko za oko ale po podvodu uz nespolupracuje

        if strategy == 7:
            # rozhodne se podle tahu soupere
            if self.spite_triggered:
                return True
                # zacina kooperaci jako prvni tah
            if not self.opponent_moves:
                return False

            return self.opponent_moves[-1]  # Tit for Tat
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
        # pro algoritmus TFT Spiteful, chci vedet ze me protihrac podvedl
        if opponent_last_move:
            self.spite_triggered = True
        # pro algorimus ORE
        reward = self.payoff_matrix[my_last_move][opponent_last_move][0]
        if my_last_move:
            self.total_reward_D += reward
            self.count_D += 1
        else:
            self.total_reward_C += reward
            self.count_C += 1
        # pro algoritmus GTFT
        if self.strategy == "GRIM" and opponent_last_move:
            self.triggered = True

class Sofie8:
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
        # pro algoritmus TFT Spiteful:
        self.spite_triggered = False
        # pro algoritmus ORE:
        self.total_reward_C = 0
        self.count_C = 0
        self.total_reward_D = 0
        self.count_D = 0
        # pro algoritmus GTFT:
        self.strategy = "GTFT"
        # pro algoritmus Adaptivni GTFT:
        self.noise_counter = 0
        self.R = payoff_matrix[0][0][0]
        self.P = payoff_matrix[1][1][0]
        self.T = payoff_matrix[1][0][0]
        self.S = payoff_matrix[0][1][0]
        self.g = min(1 - (self.T - self.R) / (self.R - self.S), (self.R - self.P) / (self.T - self.P))

    def select_move(self):
        # VRACI TRUE NEBO FALSE
        strategy = 1  # nastavim druh me strategie


        # ------------------------------------------------
        # strategie: ORE
        # -> adpatuje se podle vahy C nebo D

        # zacne kooperovat
        if self.count_C == 0 and self.count_D == 0:
            return False
        avg_C = self.total_reward_C / self.count_C if self.count_C > 0 else 0
        avg_D = self.total_reward_D / self.count_D if self.count_D > 0 else 0
        return avg_D > avg_C  # vybere tah s vyssim prumernym ziskem
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
        # pro algoritmus TFT Spiteful, chci vedet ze me protihrac podvedl
        if opponent_last_move:
            self.spite_triggered = True
        # pro algorimus ORE
        reward = self.payoff_matrix[my_last_move][opponent_last_move][0]
        if my_last_move:
            self.total_reward_D += reward
            self.count_D += 1
        else:
            self.total_reward_C += reward
            self.count_C += 1
        # pro algoritmus GTFT
        if self.strategy == "GRIM" and opponent_last_move:
            self.triggered = True

class Sofie9:
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
        # pro algoritmus TFT Spiteful:
        self.spite_triggered = False
        # pro algoritmus ORE:
        self.total_reward_C = 0
        self.count_C = 0
        self.total_reward_D = 0
        self.count_D = 0
        # pro algoritmus GTFT:
        self.strategy = "GTFT"
        # pro algoritmus Adaptivni GTFT:
        self.noise_counter = 0
        self.R = payoff_matrix[0][0][0]
        self.P = payoff_matrix[1][1][0]
        self.T = payoff_matrix[1][0][0]
        self.S = payoff_matrix[0][1][0]
        self.g = min(1 - (self.T - self.R) / (self.R - self.S), (self.R - self.P) / (self.T - self.P))

    def select_move(self):
        # VRACI TRUE NEBO FALSE
        strategy = 1  # nastavim druh me strategie

        # ------------------------------------------------
        # strategie: GTFT
        # ->

        if self.strategy == "GRIM" and self.triggered:
            return True  # DEFECT navždy

        if self.turn < 6:
            # GTFT fáze
            if self.turn == 0:
                return False  # první tah: COOPERATE
            if self.opponent_moves[-1]:
                # po zradě spolupracuje s pravděpodobností g(R,P,T,S)
                R = self.payoff_matrix[0][0][0]
                P = self.payoff_matrix[1][1][0]
                T = self.payoff_matrix[1][0][0]
                S = self.payoff_matrix[0][1][0]
                g = min(1 - (T - R) / (R - S), (R - P) / (T - P))
                return random.random() < max(0, min(1, g))
            else:
                return False  # opakuje spolupráci
        else:
            # Po 6. kole: adaptivní rozhodnutí
            defect_rate = sum(self.opponent_moves) / len(self.opponent_moves)
            if defect_rate > 0.6:
                self.strategy = "GRIM"
                self.triggered = True
                return True
            elif defect_rate > 0.3:
                self.strategy = "PAVLOV"
                if self.my_moves[-1] == self.opponent_moves[-1]:
                    return self.my_moves[-1]
                else:
                    return not self.my_moves[-1]
            else:
                self.strategy = "GTFT"
                if self.opponent_moves[-1]:
                    R = self.payoff_matrix[0][0][0]
                    P = self.payoff_matrix[1][1][0]
                    T = self.payoff_matrix[1][0][0]
                    S = self.payoff_matrix[0][1][0]
                    g = min(1 - (T - R) / (R - S), (R - P) / (T - P))
                    return random.random() < max(0, min(1, g))
                else:
                    return False
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
        # pro algoritmus TFT Spiteful, chci vedet ze me protihrac podvedl
        if opponent_last_move:
            self.spite_triggered = True
        # pro algorimus ORE
        reward = self.payoff_matrix[my_last_move][opponent_last_move][0]
        if my_last_move:
            self.total_reward_D += reward
            self.count_D += 1
        else:
            self.total_reward_C += reward
            self.count_C += 1
        # pro algoritmus GTFT
        if self.strategy == "GRIM" and opponent_last_move:
            self.triggered = True

class Sofie10:
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
        # pro algoritmus TFT Spiteful:
        self.spite_triggered = False
        # pro algoritmus ORE:
        self.total_reward_C = 0
        self.count_C = 0
        self.total_reward_D = 0
        self.count_D = 0
        # pro algoritmus GTFT:
        self.strategy = "GTFT"
        # pro algoritmus Adaptivni GTFT:
        self.noise_counter = 0
        self.R = payoff_matrix[0][0][0]
        self.P = payoff_matrix[1][1][0]
        self.T = payoff_matrix[1][0][0]
        self.S = payoff_matrix[0][1][0]
        self.g = min(1 - (self.T - self.R) / (self.R - self.S), (self.R - self.P) / (self.T - self.P))

    def select_move(self):
        # VRACI TRUE NEBO FALSE
        strategy = 1  # nastavim druh me strategie

        # ------------------------------------------------
        # strategie: Adaptivni GTFT
        # ->


        if self.strategy == "GRIM" and self.triggered:
            return True  # DEFECT navždy

        if self.turn < 6:
            # GTFT fáze
            if self.turn == 0:
                return False  # první tah: COOPERATE
            if self.opponent_moves[-1]:
                return random.random() < max(0, min(1, self.g))
            else:
                return False
        else:
            # Detekce šumu: pokud hráč spolupracoval a soupeř podvedl
            if self.my_moves[-1] == False and self.opponent_moves[-1] == True:
                self.noise_counter += 1

            # Přepnutí strategie podle chování soupeře
            defect_rate = sum(self.opponent_moves) / len(self.opponent_moves)
            if defect_rate > 0.6 and self.noise_counter < 2:
                self.strategy = "GRIM"
                self.triggered = True
                return True
            elif defect_rate > 0.3:
                self.strategy = "PAVLOV"
                if self.my_moves[-1] == self.opponent_moves[-1]:
                    return self.my_moves[-1]
                else:
                    return not self.my_moves[-1]
            else:
                self.strategy = "GTFT"
                if self.opponent_moves[-1]:
                    return random.random() < max(0, min(1, self.g))
                else:
                    return False
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
        # pro algoritmus TFT Spiteful, chci vedet ze me protihrac podvedl
        if opponent_last_move:
            self.spite_triggered = True
        # pro algorimus ORE
        reward = self.payoff_matrix[my_last_move][opponent_last_move][0]
        if my_last_move:
            self.total_reward_D += reward
            self.count_D += 1
        else:
            self.total_reward_C += reward
            self.count_C += 1
        # pro algoritmus GTFT
        if self.strategy == "GRIM" and opponent_last_move:
            self.triggered = True
