from enum import Enum
from board import Board, BLACK, WHITE
from mini_max import AgentType, AlphaBeta


class PlayerType(Enum):
    human = 'Human'
    greedy = 'Greedy'


class Player:

    def __init__(self, name):
        self.name = name

    def get_best_move(self, board: Board, max_level):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def get_type_name(self):
        pass


class HumanPlayer(Player):

    def get_best_move(self, board: Board, max_level):
        return None, 0

    def get_type_name(self):
        return 'Human'


class GreedyPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.player_type = AgentType.greedy

    def get_best_move(self, board: Board, max_level):
        agent = AlphaBeta(max_level, self.player_type)
        return agent.get_best_action_and_value(board)

    def get_type_name(self):
        return 'Greedy'
