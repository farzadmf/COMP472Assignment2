from board import Board
from enum import Enum


class AgentType(Enum):
    greedy = 'Greedy'


class AlphaBeta:

    def __init__(self, max_depth: int, agent_type: AgentType):
        self._max_depth = max_depth
        self.agent_type = agent_type

    def get_best_action_and_value(self, board: Board):
        return self.maxi_min(board, 0, float("-inf"), float("inf"))

    def maxi_min(self, board: Board, depth: int, alpha, beta):
        if depth == self._max_depth or board.is_game_over():
            evaluation_function = board.heuristics[self.agent_type]
            return None, evaluation_function()

        best_move = None
        successors = board.get_successors()

        # if len(successors) == 0:
        #     successors = board.create_pass_successor()

        for next_move, next_state in successors:
            _, value = self.mini_max(next_state, depth + 1, alpha, beta)

            if value > alpha:
                best_move, alpha = next_move, value

            if alpha >= beta:
                break

        return best_move, alpha

    def mini_max(self, board: Board, depth: int, alpha, beta):
        if depth == self._max_depth or board.is_game_over():
            evaluation_function = board.heuristics[self.agent_type]
            return None, evaluation_function()

        best_move = None
        successors = board.get_successors()

        # if len(successors) == 0:
        #     successors = board.create_pass_successor()

        for next_move, next_state in successors:
            _, value = self.maxi_min(next_state, depth + 1, alpha, beta)

            if value < beta:
                best_move, beta = next_move, value

            if alpha >= beta:
                break

        return best_move, beta
