from player import Player, PlayerType, create_player
from board import Board, BLACK, WHITE
import time
import argparse

# Valid choices for player type
player_types = [member.value for _, member in PlayerType.__members__.items() if member.value != 'Human']

# Minimum and maximum values
minimum_level = 1
maximum_level = 6
minimum_timeout = 1
maximum_timeout = 60

# Helper variables
range_meta_variable = 'Values: [{} ... {}]'

# Configure command-line arguments
parser = argparse.ArgumentParser(description='Program to Run a Series of Othello Games with Specified Features',
                                 formatter_class=argparse.RawTextHelpFormatter)
# start_state_group = parser.add_mutually_exclusive_group()

parser.add_argument('-bp', '--black_player', help='Type of the Black Player', type=str,
                    choices=player_types)
parser.add_argument('-wp', '--white_player', help='Type of the White Player', type=str,
                    choices=player_types)
parser.add_argument('-min', '--min_level', help='Minimum Level to Start with (default = 1)',
                    type=int, choices=range(minimum_level, maximum_level + 1), default=1,
                    metavar=range_meta_variable.format(minimum_level, maximum_level))
parser.add_argument('-max', '--max_level', help='Maximum Level to Reach (default = 1)',
                    type=int, choices=range(minimum_level, maximum_level + 1), default=1,
                    metavar=range_meta_variable.format(minimum_level, maximum_level))
parser.add_argument('-t', '--time_out', help='Time-out Value (in Seconds) for each Move (default = 10)',
                    type=int, choices=range(minimum_timeout, maximum_timeout + 1), default=10,
                    metavar=range_meta_variable.format(minimum_timeout, maximum_timeout))

args = parser.parse_args()


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

        move_timeout_message = 'Move Time-out Value is {} Second{}'.format(
            args.time_out, 's' if args.time_out > 1 else '')
        header_line = '+{}+'.format('-' * header_length)
        separator = '=' * separator_length
        print('\n{}\n'.format(separator))
        print(header_line)
        print('{}'.format(header))
        print(header_line)
        print()
        print(move_timeout_message)
        print('-' * len(move_timeout_message))
        print('\n')

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

            next_move, _ = current_player.get_best_move(self.board, level, self.time_out)

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
    if args.black_player is None or args.white_player is None:
        print('You must specify both player types')
        exit(1)

    black_player_type = PlayerType(args.black_player)
    white_player_type = PlayerType(args.white_player)

    black = create_player(black_player_type, 'BLACK')
    white = create_player(white_player_type, 'WHITE')

    runner = OthelloRunner()

    runner.play_series(black_player=black,
                       white_player=white,
                       min_level=args.min_level,
                       max_level=args.max_level,
                       time_out=args.time_out)
