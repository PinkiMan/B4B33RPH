__author__ = "Pinkas Matěj"
__maintainer__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__created__ = "07/10/2025"
__date__ = "07/10/2025"
__status__ = "Prototype"
__version__ = "0.1.0"
__copyright__ = ""
__license__ = ""
__credits__ = []

"""
Project: B4B33RPH
Filename: testing_players.py
Directory: homeworks/03_PD_hrac/
"""

import random

class RandomPlayer:
    """ Random Player """
    def __init__(self, matrix):
        self.matrix = matrix
        self.history = []

    @staticmethod
    def select_move():
        return random.choice([True,False])

    def record_last_moves(self,my_turn, enemy_turn):
        self.history.append([my_turn,enemy_turn])

class FalsePlayer:
    """ False player """
    def __init__(self, matrix):
        self.matrix = matrix
        self.history=[]

    @staticmethod
    def select_move():
        return False

    def record_last_moves(self,my_turn, enemy_turn):
        self.history.append([my_turn, enemy_turn])

class TruePlayer:
    """ True player """
    def __init__(self, matrix):
        self.matrix = matrix
        self.history=[]

    @staticmethod
    def select_move():
        return True

    def record_last_moves(self,my_turn, enemy_turn):
        self.history.append([my_turn, enemy_turn])

class SwapTrue:
    """ Swap True player """
    def __init__(self, matrix):
        self.matrix = matrix
        self.history = []
        self.last = True

    def select_move(self):
        self.last = not self.last
        return self.last

    def record_last_moves(self,my_turn, enemy_turn):
        self.history.append([my_turn, enemy_turn])

class SwapFalse:
    """ Swap False player """
    def __init__(self, matrix):
        self.matrix = matrix
        self.history = []
        self.last = False

    def select_move(self):
        self.last = not self.last
        return self.last

    def record_last_moves(self,my_turn, enemy_turn):
        self.history.append([my_turn, enemy_turn])

class RepeaterPlayer:
    """ Repeater Player """
    def __init__(self, matrix):
        self.matrix = matrix
        self.history = []

    def select_move(self):
        if len(self.history) == 0:
            return random.choice([True,False])
        else:
            return self.history[-1][1]

    def record_last_moves(self,my_turn, enemy_turn):
        self.history.append([my_turn,enemy_turn])

class Pavlov:
    def __init__(self, matrix):
        self.matrix = matrix
        self.history = []
        self.last = False

    def select_move(self):
        return self.last

    def record_last_moves(self,my_turn, enemy_turn):
        if my_turn == enemy_turn:
            self.last = True
        else:
            self.last = False
        self.history.append([my_turn,enemy_turn])

class BetterBetterPlayer:
    def __init__(self, matrix):
        self.matrix=matrix
        self.history = []
        self.round = 0

    def reset(self):
        self.round = 0

    def select_move(self):
        self.round += 1
        prob = (1001 - self.round) if (1001-self.round) >= 0 else 0
        return random.choices([True,False],[1000, prob])[0]

    def record_last_moves(self,my_turn,enemy_turn):
        self.history.append([my_turn,enemy_turn])

class WorseWorsePlayer:
    def __init__(self, matrix):
        self.matrix = matrix
        self.history = []
        self.round = 0

    def reset(self):
        self.round = 0

    def select_move(self):
        self.round += 1
        return random.choices([True,False],[1,self.round/1000])[0]

    def record_last_moves(self,my_turn,enemy_turn):
        self.history.append([my_turn,enemy_turn])

class Gradual:
    def __init__(self, matrix):
        self.matrix = matrix
        self.history = []
        self.rounds = 0
        self.enemy_defects = 0
        self.defect_queue = 0
        self.last_defect = 0

    def select_move(self):
        if self.rounds == 0:
            return False
        else:
            if self.defect_queue > 0:
                self.defect_queue -= 1
                if self.defect_queue == 0:
                    self.last_defect = 2
                return True
            elif self.last_defect > 0:
                self.last_defect -= 1
                return True
            else:
                return False

    def record_last_moves(self,my_turn, enemy_turn):
        self.history.append([my_turn, enemy_turn])
        self.rounds += 1

        if enemy_turn == True:
            self.enemy_defects += 1
            self.defect_queue = self.enemy_defects



class PinkiPlayer:
    """ Pinki Player """
    def __init__(self, matrix):
        self.matrix=matrix
        self.history = []

    def select_move(self):
        if self.matrix[0][0][0]+self.matrix[0][1][0]<self.matrix[1][0][0]+self.matrix[1][1][0]:
            return False
        else:
            return True

    def record_last_moves(self,my_turn,enemy_turn):
        self.history.append([my_turn,enemy_turn])

class AntiPinkiPlayer:
    """ Anti Pinki """
    def __init__(self, matrix):
        self.matrix=matrix
        self.history = []

    def select_move(self):
        if self.matrix[0][0][0]+self.matrix[0][1][0]>self.matrix[1][0][0]+self.matrix[1][1][0]:
            return False
        else:
            return True

    def record_last_moves(self,my_turn,enemy_turn):
        self.history.append([my_turn,enemy_turn])

class BestPlayerPinki:
    def __init__(self, payoff_matrix,number_of_iterations=None):
        self.matrix=payoff_matrix
        self.History=[]
        self.Enemy_True=0
        self.Enemy_False=0
        self.Round=0
        self.Swapper=0
        self.CopyCat=0
        self.Pavlov=0


    def Enemy_expected_turn(self):
        if self.Enemy_True / (self.Enemy_True + self.Enemy_False) > 0.99:  # Only True
            return True
        elif self.Enemy_False / (self.Enemy_True + self.Enemy_False) > 0.99:  # Only False
            return False
        elif self.Swapper > 5:
            return not self.History[-1]
        elif self.Pavlov >5:
            return self.History[-1][0]==self.History[-1][1]

        elif self.Enemy_True / (self.Enemy_True + self.Enemy_False) > 0.47 and self.Enemy_True / (
                self.Enemy_True + self.Enemy_False) < 0.5:
            return True
        elif self.Enemy_False / (self.Enemy_True + self.Enemy_False) > 0.47 and self.Enemy_False / (
                self.Enemy_True + self.Enemy_False) < 0.5:
            return False
        return None


    def select_move(self):
        if self.Round>10:
            Enemy_Output=self.Enemy_expected_turn()
            if Enemy_Output!=None:


                xd=self.matrix[0][int(Enemy_Output)][0]
                xd1=self.matrix[1][int(Enemy_Output)][0]

                if self.matrix[0][int(Enemy_Output)][0]>=self.matrix[1][int(Enemy_Output)][0]:
                    return False
                else:
                    return True


        if self.matrix[0][0][0]+self.matrix[0][1][0]>self.matrix[1][0][0]+self.matrix[1][1][0]: #Last
            return False
        else:
            return True



    def record_last_moves(self,my_turn,enemy_turn):
        if enemy_turn==True:
            self.Enemy_True+=1
        else:
            self.Enemy_False+=1

        if len(self.History)>0:
            if self.History[-1][1]!=enemy_turn:
                self.Swapper+=1
            else:
                self.Swapper=0

            if (self.History[-1][0]==self.History[-1][1] and enemy_turn==True) or (self.History[-1][0]!=self.History[-1][1] and enemy_turn==False):
                self.Pavlov+=1
            else:
                self.Pavlov=0


        if len(self.History) > 1:
            if self.History[-1][1]==self.History[-2][0]:
                self.CopyCat+=1
            else:
                self.CopyCat=0




        self.Round+=1
        self.History.append([my_turn,enemy_turn])


class Patrik:
    '''Hrac hraje co ho napadne'''
    def __init__(self, payoff_matrix, number_of_iterations=None):
        self.payoff = payoff_matrix[0] + payoff_matrix[1]
        self.iterations = number_of_iterations
        self.moves = []

        self.init_strategy()


    def init_strategy(self):
        '''Vybere strategii podle matice '''
        self. strat = 1
        sums = []
        self.maxsum = self.payoff[0][0] + self.payoff[0][1]
        for i, mat in enumerate(self.payoff):
            sums.append({i: mat[0] + mat[1]})
            if self.maxsum < mat[0] + mat[1]:
                self.maxsum = mat[0] + mat[1]
                self.strat = i

        if self.iterations != None:
            if self.iterations < 3:
                self.strat = 3

    def select_move(self):
        '''0: Passive, 1&2: copycat, 3: Aggressive'''
        if self.strat == 0:
            return False
        if self.strat in [1,2]:
            if len(self.moves) > 1:
                return self.moves[-1][1]
            else:
                return False
        if self.strat == 3:
            return True




    def record_last_moves(self, my_last_move, opponent_last_move):
        '''Zapamatuje si podledni tahy, zmeni strategii'''
        self.moves.append([my_last_move,opponent_last_move])
        count = 0
        if opponent_last_move == False:
            self.strat = 1
        for x in self.moves:
            if x[1] == False:
                count += 1
        if count >= 1:
            self.strat = 3

class Old:
    """Player have strategy 'Soft mayo', in speacial cases, they use payoff_matrix."""

    def __init__(self, payoff_matrix, number_of_iterations=0):
        self.payoff_matrix = payoff_matrix
        self.number_of_iterations = number_of_iterations

        self.my_last_move = None
        self.opponent_last_move = None
        self.history = []
        self.opponent_false = []
        self.opponent_true = []

    def select_move(self):
        # example:
        #   ( ((4,4),(1,6)) , ((6,1),(2,2)) )
        #   ( ((C,C),(C,D)) , ((D,C),(D,D)) )
        COOPERATE = 0
        DEFFECT = 1
        ME = 0
        CC = self.payoff_matrix[COOPERATE][COOPERATE]
        DD = self.payoff_matrix[DEFFECT][DEFFECT]
        MAX = max(self.payoff_matrix)

        if MAX == CC[ME]:
            return COOPERATE

        elif MAX == DD[ME]:
            return DEFFECT

        else:
            self.opponent_false = []
            self.opponent_true = []
            x = len(self.opponent_false)
            y = len(self.opponent_true)

            if x >= y:
                return False

            else:
                return True

    def record_last_moves(self, my_last_move, opponent_last_move):
        self.history.append([my_last_move, opponent_last_move])
        if not self.opponent_last_move:
            self.opponent_false.append([opponent_last_move])
        else:
            self.opponent_true.append([opponent_last_move])

class Luky:
    '''Hrac, ktery bude hrat na zaklade predchozich tahu protihrace.'''
    '''Snazi se soupere "kopirovat".'''

    def __init__(self, payoff_matrix, number_of_iterations = None):
        self.matrix = payoff_matrix
        self.my_moves = []
        self.opponent_move = []
        self.iteration = number_of_iterations
        self.opponent_false = 1
        self.opponent_true = 1

    def select_move(self):
        '''Podminka - reakce na souperovi minule tahy.'''
        if (len(self.opponent_move) > 0):
            if self.opponent_move[-1] == [False]:
                self.opponent_false = self.opponent_false + 1
            elif self.opponent_move[-1] == [True]:
                self.opponent_true = self.opponent_true + 1
        '''Metoda vraci True nebo False s urcitou vahou, ktera zavisi na protivnikove minulem tahu.'''
        return random.choices([True, False],[self.opponent_true,self.opponent_false])[0]

    def record_last_moves(self, my_last_move, opponent_last_move):
        self.my_moves.append(my_last_move)
        self.opponent_move.append(opponent_last_move)

class Elka1 :
    '''Hrac, ktory kopiruje posledny tah supera'''

    def __init__(self, payoff_matrix, number_of_iterations=None) :
        self.payoff_matrix = payoff_matrix
        self.number_of_iterations = number_of_iterations
        self.last_opponent_move = False     # False = spolupráca; True = podvod
        # Zaciname s predpokladom, ze super v prvom tahu spolupracuje (False).
        # Ak nemame informaciu o predoslom tahu (prvy tah), zacneme so spolupracou.

    def select_move(self) :
        # Kopirujeme predchadzajuci tah supera.
        # Ak super posledny tah podvadzal (True), podvadzame aj my.
        # Ak super posledny tah spolupracoval (False), spolupracujeme aj my.

        return self.last_opponent_move
        # Vracia hodnotu posledneho tahu supera (True = zrada, False = spolupraca).

    def record_last_moves(self, my_last_move, opponent_last_move) :
        # Zaznamename posledny tah supera, aby sme ho mohli v nasledujucom kole skopirovat.
        # Nesmie ukladat historiu, len si zapamata posledny tah.

        self.last_opponent_move = opponent_last_move
        # Ulozime posledny tah supera do premenneho atributu.

class Elka2 :
    '''Adaptive player who can change strategy based on the type of payoff matrix'''

    def __init__(self, payoff_matrix, number_of_iterations=None) :
        self.payoff_matrix = payoff_matrix
        self.number_of_iterations = number_of_iterations
        self.last_opponent_move = False  # False = cooperation; True = betrayal
        self.my_move_history = []
        self.opponent_move_history = []
        self.suspicion_threshold = 0.7  # If the opponent betrays more than 70% of the time, we switch strategy
        self.noise_probability = 0.05  # Probability of noise in the move
        self.self_play_detected = False  # Flag to detect self-play
        self.turn_count = 0  # Keep track of turns
        self.alternating_strategy = False  # Flag for alternating strategy
        self.always_betray = False  # Flag if we detect that always betraying is the best strategy

        # Detect the type of matrix
        self.detect_matrix_type ()

    def detect_matrix_type(self) :
        '''Analyze the payoff matrix to determine the optimal strategy'''
        C_C = self.payoff_matrix [0] [0]  # Payoff when both cooperate
        C_D = self.payoff_matrix [0] [1]  # Payoff when I cooperate, opponent betrays
        D_C = self.payoff_matrix [1] [0]  # Payoff when I betray, opponent cooperates
        D_D = self.payoff_matrix [1] [1]  # Payoff when both betray

        # Detect if alternating strategy is beneficial (e.g., C_D and D_C are very high)
        if C_D [1] > D_D [1] and D_C [0] > D_D [0] :
            self.alternating_strategy = True

        # Detect if always betraying is the dominant strategy
        if D_D [0] > C_D [0] and D_D [0] > C_C [0] and D_D [0] > D_C [0] :
            self.always_betray = True

    def select_move(self) :
        '''Player decides whether to cooperate (False) or betray (True)'''

        # If self-play is detected, always cooperate to maximize the total gain
        if self.self_play_detected :
            return False  # Cooperation with oneself maximizes the overall score

        # If the matrix suggests always betraying, do so
        if self.always_betray :
            return True  # Always betray if it's the best strategy

        # If an alternating strategy is beneficial, alternate between cooperation and betrayal
        if self.alternating_strategy :
            self.turn_count += 1
            return self.turn_count % 2 == 1  # Betray on odd turns, cooperate on even turns

        # If the opponent is betraying too often, start betraying too
        if self.should_betray () :
            return True  # Betray if suspicion of frequent betrayal is high

        # If it's the start of the game, assume the opponent cooperates
        if len (self.opponent_move_history) == 0 :
            return False  # Cooperation at the start

        # Copy the opponent's last move (mimicking their behavior)
        return self.last_opponent_move

    def should_betray(self) :
        '''Decide whether to start betraying based on opponent's move history'''
        # If the opponent is betraying often, switch to betrayal
        if len (self.opponent_move_history) > 0 :
            betray_count = sum (self.opponent_move_history)
            betray_rate = betray_count / len (self.opponent_move_history)
            if betray_rate > self.suspicion_threshold :
                return True
        return False

    def detect_self_play(self) :
        '''Detect if the player is playing against themselves based on move history'''
        if self.my_move_history == self.opponent_move_history :
            self.self_play_detected = True

    def handle_noise(self, opponent_last_move) :
        '''Accounts for the possibility of noise in communication'''
        if random.random () < self.noise_probability :
            # Invert the opponent's move if noise occurs
            return not opponent_last_move
        return opponent_last_move

    def record_last_moves(self, my_last_move, opponent_last_move) :
        '''Records moves and adjusts decision-making based on them'''
        # Save the last moves to history
        self.my_move_history.append (my_last_move)
        self.opponent_move_history.append (opponent_last_move)

        # Check if the player is playing against themselves
        self.detect_self_play ()

        # Account for noise and record the opponent's move
        self.last_opponent_move = self.handle_noise (opponent_last_move)


from typing import Optional, List, Tuple
COOPERATE = False
DEFECT = True
class GPTPlayer:
    ''' GPT player '''

    def __init__(self, payoff_matrix, number_of_iterations: Optional[int] = None):
        """
        payoff_matrix: 2x2 seznam dvojic (moje, soupeřova odměna)
        number_of_iterations: počet tahů ve hře (může být None)
        """
        self.payoff_matrix = payoff_matrix
        self.number_of_iterations = number_of_iterations
        self.history: List[Tuple[bool, bool]] = []

        # Extrahujeme základní hodnoty z matice
        self.R = payoff_matrix[0][0][0]  # reward (C,C)
        self.T = payoff_matrix[1][0][0]  # temptation (D,C)
        self.S = payoff_matrix[0][1][0]  # sucker's payoff (C,D)
        self.P = payoff_matrix[1][1][0]  # punishment (D,D)

    def select_move(self) -> bool:
        """Vrátí False=COOPERATE nebo True=DEFECT."""
        if not self.history:
            return COOPERATE  # začínáme spoluprací

        _, opp_last = self.history[-1]

        # Tit-for-Tat: zopakuju, co udělal soupeř
        intended = opp_last

        # Odpuštění při šumu: 10% šance, že budu spolupracovat i když soupeř zradil
        if intended == DEFECT and random.random() < 0.1:
            intended = COOPERATE

        # Pokud matice jasně zvýhodňuje DEFECT (T hodně > R), preferuj zradu
        if self.T > self.R + 1:
            return DEFECT

        return intended

    def record_last_moves(self, my_last_move: bool, opponent_last_move: bool):
        """Uloží poslední tahy (můj, soupeřův)."""
        self.history.append((my_last_move, opponent_last_move))

# player.py
import random
from typing import Optional, List, Tuple

COOPERATE = False
DEFECT = True

class GPT2:
    '''Adaptivní mix: handshake, Pavlov/TFT, gradual, forgiveness, opatrný endgame'''
    def __init__(self, payoff_matrix, number_of_iterations: Optional[int] = None):
        """
        payoff_matrix: 2x2 list of pairs payoff_matrix[i][j] = (payoffA, payoffB)
                       i,j in {0(C),1(D)}.
        number_of_iterations: optional known number of kol (N).
        """
        self.payoff_matrix = payoff_matrix
        self.number_of_iterations = number_of_iterations

        # Extract canonical payoffs for player A (safe fallback if format unexpected)
        try:
            self.R = payoff_matrix[0][0][0]  # C,C
            self.S = payoff_matrix[0][1][0]  # C,D (sucker)
            self.T = payoff_matrix[1][0][0]  # D,C (temptation)
            self.P = payoff_matrix[1][1][0]  # D,D (punishment)
        except Exception:
            # reasonable defaults
            self.R, self.S, self.T, self.P = 3, 0, 5, 1

        # history and stats
        self.history: List[Tuple[bool, bool]] = []
        self.total_rounds = 0
        self.opp_coop_count = 0
        self.opp_defect_count = 0

        # queue for planned moves (for Gradual punishment / queued calm)
        self._queue: List[bool] = []

        # last moves
        self._last_my: Optional[bool] = None
        self._last_opp: Optional[bool] = None

        # RNG
        self._rng = random.Random()

        # parameters (tuneable)
        self.forgiveness_rate = 0.08   # pravděpodobnost odpustit jedno defektování
        self.handshake_len = 2         # první N tahů cooperate (handshake)
        self.self_detect_window = 12   # okno pro detekci self-play / mirror
        self.min_detection_rounds = 6  # minimální kola před rozhodnutím o typech
        # store mirror hits
        self._mirror_hits = 0

        # track opponent defection events count (for Gradual)
        self._opp_defection_events = 0

    def select_move(self) -> bool:
        """Vrátí False=COOPERATE nebo True=DEFECT."""
        # pokud máme naplánované tahy (např. trestní sekvence), použij je
        if self._queue:
            return self._queue.pop(0)

        # handshake: začínáme snažit se navázat kooperaci
        if not self.history and self.handshake_len >= 1:
            return COOPERATE
        if len(self.history) < self.handshake_len:
            return COOPERATE

        # index aktuálního kola (1-based)
        round_index = len(self.history) + 1

        # ---- detekce typů soupeře ----
        opp_coop_rate = self.opp_coop_count / max(1, self.total_rounds)
        opp_def_rate = self.opp_defect_count / max(1, self.total_rounds)

        is_all_coop = (self.total_rounds >= self.min_detection_rounds and opp_coop_rate > 0.98)
        is_all_defect = (self.total_rounds >= self.min_detection_rounds and opp_def_rate > 0.98)

        # mirror detection: soupeř často hraje to, co jsem hrál v předchozím tahu
        mirror_score = self._compute_mirror_score()
        is_mirror = (self.total_rounds >= self.min_detection_rounds and mirror_score > 0.85)

        # self-play detection: pokud opponentova historie téměř přesně kopíruje moje tahy (posunutě),
        # je velká šance, že hraji proti sobě (stejná strategie).
        is_self_like = (self.total_rounds >= self.self_detect_window and mirror_score > 0.9)

        # ---- endgame logic (opatrně) ----
        if self.number_of_iterations is not None:
            # pokud víme, že jsme v posledním kole, zvaž defekt pro zisk, jen pokud:
            # - opponent dlouhodobě kooperuje AND
            # - není detekován self-play (nechceme snížit self-play sumu)
            if round_index == self.number_of_iterations:
                if (opp_coop_rate > 0.9) and (not is_self_like):
                    return DEFECT
                # pokud je self-like nebo opponent nereálně smíšený, raději cooperate
                return COOPERATE
            # optionally: ve dvou posledních kolech můžeme být opatrnější; implementováno jen 1-kolo

        # ---- jednoduchý Pavlov (win-stay/lose-shift) ----
        if self._last_my is None:
            pavlov_choice = COOPERATE
        else:
            last_pay = self.payoff_matrix[int(self._last_my)][int(self._last_opp)][0]
            # považujeme za "dobré" pokud >= průměr mezi R a T (heuristika)
            good_threshold = (self.R + self.T) / 2.0
            if last_pay >= good_threshold:
                pavlov_choice = self._last_my
            else:
                pavlov_choice = not self._last_my

        # ---- behavior by detected type ----
        # 1) always-cooperate -> malé, řízené exploitování
        if is_all_coop:
            # exploit s nízkou pravděpodobností; adaptivně podle (T-R)
            extra = max(0.0, (self.T - self.R) / max(1.0, abs(self.R) + 1.0))
            prob_defect = min(0.30, 0.10 + 0.18 * extra)  # nikdy příliš agresivní
            if self._rng.random() < prob_defect and (not is_self_like):
                return DEFECT
            return COOPERATE

        # 2) always-defect -> bránit se
        if is_all_defect:
            return DEFECT

        # 3) mirror/TFT-like -> kopíruj jeho poslední tah (stabilní)
        if is_mirror:
            tft_move = self.history[-1][1]
            # pokud pavlov a tft souhlasí, použij; pokud ne, preferuj tft pro stabilitu
            base = tft_move
            # forgiveness: občas odpustit
            if base == DEFECT and self._rng.random() < self.forgiveness_rate:
                return COOPERATE
            return base

        # 4) nejasný / směsný soupeř: rozhodni podle očekávaného zisku + Pavlov
        exp_coop = opp_coop_rate * self.R + (1 - opp_coop_rate) * self.S
        exp_def  = opp_coop_rate * self.T + (1 - opp_coop_rate) * self.P

        # Pokud defection dává jasně více, použij ji; ale respektuj Pavlov
        if exp_def > exp_coop + 1e-9:
            # pokud pavlov_choice je také defekt, jasně defect; jinak použij většinou defect
            if pavlov_choice == DEFECT:
                return DEFECT
            else:
                if self._rng.random() < 0.85:
                    return DEFECT
                else:
                    return COOPERATE

        # 5) default: Pavlov + malé odpuštění a drobná náhodnost
        choice = pavlov_choice
        # forgiveness: pokud chceme defectovat, občas odpustíme
        if choice == DEFECT and self._rng.random() < self.forgiveness_rate:
            choice = COOPERATE
        # drobná náhodnost pro rozbití cyklů
        if self._rng.random() < 0.01:
            choice = not choice
        return choice

    def record_last_moves(self, my_last_move: bool, opponent_last_move: bool):
        """Ulož moje a soupeřovy poslední tahy (booleany)."""
        self.history.append((my_last_move, opponent_last_move))
        self.total_rounds += 1
        if opponent_last_move == COOPERATE:
            self.opp_coop_count += 1
        else:
            self.opp_defect_count += 1
            # increment defection event count and possibly schedule Gradual punishment
            self._opp_defection_events += 1
            # plán Gradual trestu: po k-té defekci soupeře přidat k defektů + 2 coop
            # ale capneme tresty, abychom nerušili příliš dlouho
            max_n = 4
            n = min(max_n, self._opp_defection_events)
            punishment = [DEFECT] * n + [COOPERATE, COOPERATE]
            # připojíme za současnou frontu
            # (pokud hra je v pokročilém stádiu self-play, možná nechceme trestat => kontrolujeme)
            # pokud detekujeme, že soupeř je pravděpodobně self-like, neplánujeme trest
            if not self._likely_self_play():
                # zkracujeme frontu, aby trestní fronta nebyla nekonečná
                space_left = 12 - len(self._queue)
                if space_left > 0:
                    self._queue.extend(punishment[:space_left])

        # update mirror hits metric
        if len(self.history) >= 2:
            # pokud opponent's current move == my previous => mirror "hit"
            if self.history[-1][1] == self.history[-2][0]:
                self._mirror_hits += 1

        # uložit poslední tahy
        self._last_my = my_last_move
        self._last_opp = opponent_last_move

    # ---- pomocné metody ----
    def _compute_mirror_score(self) -> float:
        """Vrátí poměr mirror hits v rámci posledního okna."""
        w = min(self.self_detect_window, len(self.history))
        if w < 2:
            return 0.0
        hits = 0
        checks = 0
        start = len(self.history) - w
        for i in range(start + 1, len(self.history)):
            # porovnat my_move_{i-1} a opp_move_{i}
            my_prev = self.history[i-1][0]
            opp_now = self.history[i][1]
            checks += 1
            if opp_now == my_prev:
                hits += 1
        return (hits / checks) if checks > 0 else 0.0

    def _likely_self_play(self) -> bool:
        """Rychlá heuristika: zda je pravděpodobné, že hrajeme proti sobě."""
        if self.total_rounds < self.self_detect_window:
            return False
        mirror_score = self._compute_mirror_score()
        # velmi vysoký mirror score => pravděpodobně self-play (nebo mirror strategy)
        return mirror_score > 0.92



class Tournament:
    def __init__(self, players, payoff_matrix, rounds=10_000):
        self.players = players
        self.rounds = rounds
        self.payoff_matrix = payoff_matrix
        self.points = {}
        self.enemy_points = {}
        self.table_points = {}
        self.solo_points = {}
        self.print_players = 15

    def game(self, player_1, player_2):
        p1 = 0
        p2 = 0

        for _ in range(self.rounds):
            move1 = player_1.select_move()
            move2 = player_2.select_move()

            p1 += self.payoff_matrix[int(move1 == True)][int(move2 == True)][0]
            p2 += self.payoff_matrix[int(move1 == True)][int(move2 == True)][1]

            player_1.record_last_moves(move1, move2)
            player_2.record_last_moves(move2, move1)

        return p1, p2

    def tournament_self(self):
        for player_1 in self.players:
            player1 = player_1(self.payoff_matrix)
            player2 = player_1(self.payoff_matrix)
            score1, score2 = self.game(player1, player2)

            name_1 = player1.__class__.__name__

            if name_1 in self.solo_points.keys():
                self.solo_points[name_1] += score1
                self.solo_points[name_1] += score2
            else:
                self.solo_points[name_1] = score1
                self.solo_points[name_1] += score2


        sorted_dict = dict(sorted(self.solo_points.items(), key=lambda x: x[1])[
                               :(len(self.solo_points.items()) - 1) - self.print_players:-1])


        #print("Points ballance:")
        ballance_dict = {}
        for key in self.solo_points.keys():
            ballance_dict[key] = self.solo_points[key] - self.solo_points[key]

        for key in sorted_dict.keys():
            #print(f"\t{str(key).ljust(20)} - \t{self.solo_points[key]}")
            pass

        score_dict = {}
        i = 0
        last_points = 0
        for index, key in enumerate(sorted_dict.keys()):
            if last_points != self.solo_points[key]:
                last_points = self.solo_points[key]
                i += 1
            score_dict[key] = i

        return score_dict

    def tournament(self):
        for index_1, player_1 in enumerate(self.players):
            for index_2, player_2 in enumerate(self.players):
                if index_1==index_2:
                    continue

                player1 = player_1(self.payoff_matrix)
                player2 = player_2(self.payoff_matrix)
                score1, score2 = self.game(player1, player2)

                name_1 = player1.__class__.__name__
                name_2 = player2.__class__.__name__

                if name_1 in self.points.keys():
                    self.points[name_1] += score1
                    self.enemy_points[name_1] += score2
                else:
                    self.points[name_1] = score1
                    self.enemy_points[name_1] = score2

                if name_2 in self.points.keys():
                    self.points[name_2] += score2
                    self.enemy_points[name_2] += score1
                else:
                    self.points[name_2] = score2
                    self.enemy_points[name_2] = score1


                self.table_points[f"{name_1}:{name_2}"] = (score1, score2)


                #print(f"\t{player1.__class__.__name__}:\t{player2.__class__.__name__} - {score1/self.rounds}/{score2/self.rounds}")

        """#print("Points get:")
        sorted_dict = dict(sorted(self.points.items(), key=lambda x: x[1])[:(len(self.points.items())-1)-self.print_players:-1])
        for key in sorted_dict.keys():
            #print(f"\t{key}:\t{self.points[key]}")
            pass

        #print("Points given:")
        sorted_dict = dict(sorted(self.enemy_points.items(), key=lambda x: x[1])[:self.print_players])
        for key in sorted_dict.keys():
            #print(f"\t{key}:\t{self.enemy_points[key]}")
            pass"""

        #print("Points ballance:")
        ballance_dict = {}
        for key in self.points.keys():
            ballance_dict[key] = self.points[key] - self.enemy_points[key]
        sorted_dict = dict(
            sorted(ballance_dict.items(), key=lambda x: x[1])[::-1])
        for key in sorted_dict.keys():
            # print(f"\t{str(key).ljust(20)} - \t{self.points[key]}:{self.enemy_points[key]}:{ballance_dict[key]}")
            pass



        """import matplotlib.pyplot as plt

        x = [i for i in range(len(sorted_dict.keys()))]
        y1 = [self.points[key] for key in sorted_dict.keys()]
        y2 = [self.enemy_points[key] for key in sorted_dict.keys()]
        y3 = [ballance_dict[key] for key in sorted_dict.keys()]

        fig, ax = plt.subplots()

        ax.plot(x, y1, color='b')
        ax.plot(x, y2, color='r')
        ax.plot(x, y3, color='y')

        ax.scatter(x, y1, color='b')
        ax.scatter(x, y2, color='r')
        ax.scatter(x, y3, color='y')

        plt.show()"""

        score_dict = {}
        for index, key in enumerate(sorted_dict.keys()):
            score_dict[key] = index

        return score_dict


def main():
    from player import MyPlayer
    players = [RandomPlayer, FalsePlayer, TruePlayer, SwapTrue, SwapFalse, GPTPlayer, PinkiPlayer, AntiPinkiPlayer,
               BestPlayerPinki, RepeaterPlayer, Pavlov, BetterBetterPlayer, WorseWorsePlayer, Patrik, Old, Luky, Gradual, Elka1, Elka2, GPT2, MyPlayer]

    payoff_matrix_1 = [[(4, 4), (1, 6)], [(6, 1), (2, 2)]]
    payoff_matrix_2 = [[(4, 4), (3, 10)], [(10, 3), (2, 2)]]
    payoff_matrix_3 = [[(1, 1), (2, 3)], [(3, 2), (5, 5)]]
    payoff_matrix_4 = [[(5, 5), (3, 2)], [(2, 3), (1, 1)]]
    payoff_matrix_5 = (((4, 4), (1, 6)), ((6, 1), (2, 2)))
    payoff_matrix_6 = [[(2, 2), (4, 6)], [(6, 4), (10, 10)]]
    payoff_matrix_7 = [[(5, 5), (1, 70)], [(70, 1), (2, 2)]]

    payoff_matrix_list = [payoff_matrix_1, payoff_matrix_2, payoff_matrix_3, payoff_matrix_4, payoff_matrix_5,
                          payoff_matrix_6, payoff_matrix_7]

    score_dict = {}
    print("me vs all")
    for _ in range(100):
        turn = Tournament(players=players, payoff_matrix=random.choice(payoff_matrix_list), rounds=random.randint(90,1000))
        turn_score_dict = turn.tournament()
        for key in turn_score_dict.keys():
            if key in score_dict:
                score_dict[key] += turn_score_dict[key]
            else:
                score_dict[key] = turn_score_dict[key]

    sorted_dict = dict(
        sorted(score_dict.items(), key=lambda x: x[1]))
    for key in sorted_dict.keys():
        print(key, score_dict[key])

    "========================================================="

    score_dict = {}
    print("\nme vs me")
    for _ in range(100):
        turn = Tournament(players=players, payoff_matrix=random.choice(payoff_matrix_list),
                          rounds=random.randint(90, 1000))
        turn_score_dict = turn.tournament_self()
        for key in turn_score_dict.keys():
            if key in score_dict:
                score_dict[key] += turn_score_dict[key]
            else:
                score_dict[key] = turn_score_dict[key]

    sorted_dict = dict(
        sorted(score_dict.items(), key=lambda x: x[1]))
    for key in sorted_dict.keys():
        print(key, score_dict[key])

    # print(f"\n{turn.table_points}\n")

if __name__ == '__main__':
    main()
    exit()
    payoff_matrix = [[(4, 4), (1, 6)], [(6, 1), (2, 2)]]
    player = Gradual(payoff_matrix)

    p1 = 0
    p2 = 0
    for i in range(20):
        move_1 = player.move()
        move_2 = True if input('play: ') == 't' else False

        p1 += payoff_matrix[int(move_1 == True)][int(move_2 == True)][0]
        p2 += payoff_matrix[int(move_1 == True)][int(move_2 == True)][1]

        player.record_last_moves(move_1, move_2)

        print(move_1, move_2)
