from enum import Enum
from board import Board, BLACK, WHITE
from mini_max import AgentType, AlphaBeta


class PlayerType(Enum):
    human = 'Human'
    greedy = 'Greedy'
    simple = 'Simple'
    composite = 'Composite'
    mobile = 'Mobile'
    greedy = 'Greedy'


class Player:

    def __init__(self, name):
        self.name = name
        self.agent = None  # type: AlphaBeta

    def get_best_move(self, board: Board, max_level, time_out):
        self.agent = AlphaBeta(max_level, self.player_type)
        return self.agent.get_best_action_and_value(board, time_out)

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


class SimplePlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.player_type = AgentType.simple

    def get_type_name(self):
        return 'Simple'


class CompositePlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.player_type = AgentType.composite

    def get_type_name(self):
        return 'Composite'

class MobilePlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.player_type = AgentType.mobile

    def get_type_name(self):
        return 'Mobile'

class CornerPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.player_type = AgentType.corner

    def get_type_name(self):
        return 'Corner'

def create_player(player_type: PlayerType, player_name: str):
    """
    Create a player based on the type
    :param player_type: type of the player to be created
    :param player_name: name of the player to be created
    :return: player object
    """
    if player_type == PlayerType.human:
        return HumanPlayer(player_name)
    if player_type == PlayerType.greedy:
        return GreedyPlayer(player_name)
    if player_type == PlayerType.simple:
        return SimplePlayer(player_name)
    if player_type == PlayerType.composite:
        return CompositePlayer(player_name)
    if player_type == PlayerType.mobile:
        return MobilePlayer(player_name)
    if player_type == PlayerType.corner:
        return CornerPlayer(player_name)
