from player import Player, PlayerType, HumanPlayer, GreedyPlayer
from board import Board, BLACK, WHITE
import time


class OthelloRunner:

    def __init__(self):
        self.board = None
        self.players = dict()
        self.scores = dict()

        self.winner = 0

        self.wins = dict()
        self.wins[BLACK] = 0
        self.wins[WHITE] = 0
        self.ties = 0

    def play_series(self, black_player: Player, white_player: Player, min_level: int, max_level: int):
        separator_length = 87
        header = "| Running games using {} with levels from '{}' to '{}' |"

        if type(black_player) == type(white_player):
            header = header.format('two {} players'.format(black_player.get_type_name()), min_level, max_level)
        else:
            header = header.format('one {} player and one {} player'.format(
                black_player.get_type_name(), white_player.get_type_name()), min_level, max_level)

        header_line = '+{}+'.format('-' * (len(header) - 2))
        separator = '=' * separator_length
        print('\n{}\n'.format(separator))
        print(header_line)
        print('{}'.format(header))
        print(header_line)
        print()

        for level in range(min_level, max_level + 1):
            self.board = Board()
            self.players[BLACK] = black_player
            self.players[WHITE] = white_player
            self.scores[BLACK] = 0
            self.scores[WHITE] = 0
            self._play_game(level)

        self.print_final_results()
        print('\n{}\n'.format(separator))

    def _play_game(self, level: int):
        print("Running game with level: '{}': ".format(level), end='')

        start_time = time.time()
        while not self.board.is_game_over():
            # print(self.board)
            # print(Board.get_color_string(self.board.get_turn()))
            # input()
            current_player = self.players[self.board.get_turn()]  # type: Player
            next_move, _ = current_player.get_best_move(self.board, level)
            self.board = self.board.execute_move(next_move)
        end_time = time.time()

        self.scores[BLACK], self.scores[WHITE] = self.board.get_final_score()
        if self.scores[BLACK] == self.scores[WHITE]:
            self.ties += 1
            self.winner = 0
        elif self.scores[BLACK] > self.scores[WHITE]:
            self.wins[BLACK] += 1
            self.winner = BLACK
        else:
            self.wins[WHITE] += 1
            self.winner = WHITE

        if self.scores[BLACK] == self.scores[WHITE]:
            print(' The game was a tie', end='')
        else:
            print(" '{}' defeats '{}'. Score: {:2} to {:2}".format(
                Board.get_color_string(self.winner), Board.get_color_string(-self.winner),
                self.scores[self.winner], self.scores[-self.winner]
            ), end='')

        print(' (time: {:6.3}s)'.format(end_time - start_time))

    def print_final_results(self):
        print('\nFinal Results:')
        print('\t{:23} {}\n\t{:23} {}\n\t{:23} {}'.format(
            'Number of black wins:', self.wins[BLACK],
            'Number of white wins:', self.wins[WHITE],
            'Number of ties:', self.ties))


if __name__ == '__main__':
    tester = OthelloRunner()

    tester.play_series(black_player=GreedyPlayer('black'),
                       white_player=GreedyPlayer('white'),
                       min_level=1,
                       max_level=2)
