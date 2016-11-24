from player import Player, GreedyPlayer, CompositePlayer
from board import Board, BLACK, WHITE
import time


class OthelloRunner:

    def __init__(self):
        self.board = None
        self.players = dict()
        self.scores = dict()

        self.winner = 0

        self.wins = dict()
        self.ties = 0
        self.time_out = 0

    def play_series(self, black_player: Player, white_player: Player, min_level: int, max_level: int, time_out: int):
        self.wins[BLACK] = 0
        self.wins[WHITE] = 0
        self.time_out = time_out

        separator_length = 89

        if type(black_player) == type(white_player):
            header = "| Running games using two {} players with levels from '{}' to '{}' |".format(
                black_player.get_type_name(), min_level, max_level)
            header_length = len(header) - 2
        else:
            header1 = "| Running games using {} with |"
            header1 = header1.format('one {} player (BLACK) and one {} player (WHITE)'.format(
                black_player.get_type_name(), white_player.get_type_name()))
            header2 = "|          levels from '{}' to '{}'".format(min_level, max_level)
            header2 += ' ' * (len(header1) - len(header2) - 1) + '|'
            header = '{}\n{}'.format(header1, header2)
            header_length = len(header1) - 2

        header_line = '+{}+'.format('-' * header_length)
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

            next_move, _ = current_player.get_best_move(self.board, level, self.time_out,
                                                        raise_exception=False)

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
            print('{:43}'.format(' The game was a tie'), end='')
        else:
            print('{:43}'.format(" '{}' defeats '{}'. Score: {:2} to {:2}".format(
                Board.get_color_string(self.winner), Board.get_color_string(-self.winner),
                self.scores[self.winner], self.scores[-self.winner]
            )), end='')

        elapsed_time = end_time - start_time
        print(' (time: {:7.3}s)'.format(elapsed_time))

    def print_final_results(self):
        print('\nFinal Results:')
        print('\t{:23} {}\n\t{:23} {}\n\t{:23} {}'.format(
            'Number of black wins:', self.wins[BLACK],
            'Number of white wins:', self.wins[WHITE],
            'Number of ties:', self.ties))


if __name__ == '__main__':
    tester = OthelloRunner()

    minimum = 1
    maximum = 5
    time_out_value = 1

    tester.play_series(black_player=GreedyPlayer('black'),
                       white_player=GreedyPlayer('white'),
                       min_level=minimum,
                       max_level=maximum,
                       time_out=time_out_value)

    tester.play_series(black_player=CompositePlayer('black'),
                       white_player=GreedyPlayer('white'),
                       min_level=minimum,
                       max_level=maximum,
                       time_out=time_out_value)

    tester.play_series(black_player=CompositePlayer('black'),
                       white_player=CompositePlayer('white'),
                       min_level=minimum,
                       max_level=maximum,
                       time_out=1)
