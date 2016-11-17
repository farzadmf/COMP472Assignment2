from board import Board
from mini_max import AlphaBeta, AgentType
from enum import Enum

BLACK = -1
WHITE = 1


class PlayerType(Enum):
    human = 'Human'
    greedy = 'Greedy'


class Player:

    def __init__(self, name, color):
        self.name = name
        self.color = color

    def get_best_move(self, board: Board, max_level):
        pass

    def __str__(self):
        return '{} [{}]'.format(self.name, 'Black' if self.color == BLACK else 'White')


class HumanPlayer(Player):

    def get_best_move(self, board: Board, max_level):
        return None, 0


class GreedyPlayer(Player):

    def __init__(self, name, color):
        super().__init__(name, color)
        self.player_type = AgentType.greedy

    def get_best_move(self, board: Board, max_level):
        agent = AlphaBeta(max_level, self.player_type)
        return agent.get_best_action_and_value(board)
