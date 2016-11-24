from enum import Enum
from board import Board, BLACK, WHITE
from mini_max import AgentType, AlphaBeta


class PlayerType(Enum):
    human = 'Human'
    greedy = 'Greedy'
    composite = 'Composite'


class Player:

    def __init__(self, name):
        self.name = name
        self.agent = None  # type: AlphaBeta

    def get_best_move(self, board: Board, max_level, time_out, raise_exception=True):
        self.agent = AlphaBeta(max_level, self.player_type)
        return self.agent.get_best_action_and_value(board, time_out, raise_exception)

    def stop_move(self):
        self.agent.stop = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def get_type_name(self):
        pass


class HumanPlayer(Player):

    def get_best_move(self, board: Board, max_level, time_out):
        return None, 0

    def get_type_name(self):
        return 'Human'


class GreedyPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.player_type = AgentType.greedy

    def get_type_name(self):
        return 'Greedy'


class CompositePlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.player_type = AgentType.composite

    def get_type_name(self):
        return 'Composite'
