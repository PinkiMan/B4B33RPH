import random

class Sofie11:
    '''Analyzuji matici, chovani soupere i sebe a volim optimalni strategii'''


    # VYSLEDKY POZOROVANI:
    # DRUHY STRATEGIE: Tit for Tat , Detective , Grim Trigger , Win-Stay-Lose-Shift, Pavlov , Adaptive , TFT Spiteful , ORE , GTFT , Adaptivni GTFT
    # po testovani techto algoritmu, mel nejlepsi vysledky Grim Trigger
    # dle techto vysledku jsem vytvoria vlastni strategii, ktera se snazi zamerit i na poznani sebe sama, aby mela lepsi vysledky


    def __init__(self, payoff_matrix, number_of_iterations=None):
        self.payoff_matrix = payoff_matrix #((4,4), (1,6)), ((6,1), (2,2))
        self.number_of_iterations = number_of_iterations # dobre pro ruzne strategie, kde je potreba znat iterace
        self.my_moves = [] # uklada zde me tahy, abych se k nim pak mohla vracet
        self.opponent_moves = [] # uklada zde protihracovi tahy, abych se k nim pak mohla vracet
        self.turn = 0 
        self.triggered = False 
        self.playing_against_self = False
        self.strategy = "GTFT"

        # Vypocet hodnot z payoff matice
        self.R = payoff_matrix[0][0][0]  # COOP/COOP
        self.S = payoff_matrix[0][1][0]  # COOP/DEFECT
        self.T = payoff_matrix[1][0][0]  # DEFECT/COOP
        self.P = payoff_matrix[1][1][0]  # DEFECT/DEFECT

        # Vsechny mozny kombinace vzajemnych tahu
        self.total_CC = payoff_matrix[0][0][0] + payoff_matrix[0][0][1]
        self.total_DD = payoff_matrix[1][1][0] + payoff_matrix[1][1][1]
        self.total_CD = payoff_matrix[0][1][0] + payoff_matrix[0][1][1]
        self.total_DC = payoff_matrix[1][0][0] + payoff_matrix[1][0][1]

        # Ulozim si nejlepsi kombinaci tahu, ktery chci zahrat
        self.best_combo = max(("CC", self.total_CC),("DD", self.total_DD),("CD", self.total_CD),("DC", self.total_DC),key=lambda x: x[1])[0]

        # Zjisti pravdepodobnost spoluprace dle GTFT teorie
        self.g = min(1 - (self.T - self.R) / (self.R - self.S), (self.R - self.P) / (self.T - self.P))

        # Rozpoznani typu payoff matice a nasledne strategie
        if self.T > self.R > self.P > self.S:
            self.matrix_type = "classic_dilemma"
        elif self.R > self.T and self.R > self.P:
            self.matrix_type = "cooperation_favored"
        else:
            self.matrix_type = "aggressive"


    def select_move(self):
        # Nejdriv poznam zda jsem to ja sama nebo oponent
        if self.turn >= 6 and self.my_moves == self.opponent_moves:
            self.playing_against_self = True

        # Pokud hraju proti sobe, hledam nejvyhodnejsi strategii
        if self.playing_against_self:
            if self.best_combo == "CC":
                return False  # COOPERATE
            elif self.best_combo == "DD":
                return True   # DEFECT
            elif self.best_combo == "CD":
                return self.turn % 2 == 0  # sudy tah: DEFECT, lichy tah: COOPERATE
            elif self.best_combo == "DC":
                return self.turn % 2 == 1  # lichy tah: COOPERATE, lichy tah: DEFECT

        # Volba strategie pro prvni tah
        if self.matrix_type == "cooperation_favored":
            return False  # COOPERATE
        if self.matrix_type == "aggressive":
            return True  # DEFECT


        # STRATEGY = GRIM
        if self.strategy == "GRIM" and self.triggered:
            return True  # DEFECT 

        # STRATEGY = GTFT
        if self.turn < 6:
            # GTFT faze na zacatku
            if self.turn == 0:
                return False
            if self.opponent_moves[-1]:
                return random.random() < max(0, min(1, self.g)) # rozhoduje nahodne s pravdepodobnosti spoluprace
            else:
                return False
            
        else:
            # Detekce sumu - po sesti tazich se snazim zjistit jakou mel strategii
            if self.my_moves[-1] == False and self.opponent_moves[-1] == True:
                self.noise_counter = getattr(self, "noise_counter", 0) + 1
            else:
                self.noise_counter = getattr(self, "noise_counter", 0)

            # Vypocitam miru podvodu vuci celkovym tahum
            defect_rate = sum(self.opponent_moves) / len(self.opponent_moves)

            # Zahajim trategii GRIM, pokud jsem byla casto podvedena
            if defect_rate > 0.6 and self.noise_counter < 2:
                self.strategy = "GRIM"
                self.triggered = True
                return True
            
            # STRATEGIE = PAVLOV
            elif defect_rate > 0.3:
                self.strategy = "PAVLOV"
                if self.my_moves[-1] == self.opponent_moves[-1]:
                    return self.my_moves[-1]
                else:
                    return not self.my_moves[-1]
            # Pokracuju v GTFT, pokud byl souper kooperativni
            else:
                self.strategy = "GTFT"
                if self.opponent_moves[-1]:
                    return random.random() < max(0, min(1, self.g))
                else:
                    return False

    def record_last_moves(self, my_last_move, opponent_last_move):
        self.my_moves.append(my_last_move) # ukladam me posledni tahy
        self.opponent_moves.append(opponent_last_move) # ukladam oponentovy tahy
        self.turn += 1

        # Byla jsem podvedena?
        if opponent_last_move:
            self.triggered = True
