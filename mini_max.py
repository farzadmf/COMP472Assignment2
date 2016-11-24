from enum import Enum
import time


class TimeOutException(Exception):
    pass


class AgentType(Enum):
    greedy = 'Greedy'
    composite = 'Composite'


class AlphaBeta:

    def __init__(self, max_depth: int, agent_type: AgentType):
        self._max_depth = max_depth
        self.agent_type = agent_type
        self.start_time = 0
        self.time_out = 0

    def get_best_action_and_value(self, board, time_out):
        self.start_time = time.time()
        self.time_out = time_out
        return self.maxi_min(board, 0, float("-inf"), float("inf"))

    def maxi_min(self, board, depth: int, alpha, beta):
        if time.time() - self.start_time > self.time_out:
            raise TimeOutException()

        if depth == self._max_depth or board.is_game_over():
            evaluation_function = board.heuristics[self.agent_type]
            return None, evaluation_function()

        best_move = None
        successors = board.get_successors()

        for next_move, next_state in successors:
            _, value = self.mini_max(next_state, depth + 1, alpha, beta)

            if value > alpha:
                best_move, alpha = next_move, value

            if alpha >= beta:
                break

        return best_move, alpha

    def mini_max(self, board, depth: int, alpha, beta):
        if time.time() - self.start_time > self.time_out:
            raise TimeOutException()

        if depth == self._max_depth or board.is_game_over():
            evaluation_function = board.heuristics[self.agent_type]
            return None, evaluation_function()

        best_move = None
        successors = board.get_successors()

        for next_move, next_state in successors:
            _, value = self.maxi_min(next_state, depth + 1, alpha, beta)

            if value < beta:
                best_move, beta = next_move, value

            if alpha >= beta:
                break

        return best_move, beta
