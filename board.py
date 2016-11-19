"""
++++++++++++++++++++++++++++++++++++
code for the board adopted from:
https://github.com/LinxiFan/Reversi
++++++++++++++++++++++++++++++++++++

Author: Eric P. Nichols
Date: Feb 8, 2008.

Board class.

Board data:
  1 = white, -1 = black, 0 = empty
  first dim is column, 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.


Squares are stored and manipulated as (x,y) tuples. 
x is the column, y is the row.
"""
from mini_max import AgentType

BLACK = -1
WHITE = 1


class Board:
    # List of all 8 directions on the board, as (x,y) offsets
    __directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

    def __init__(self, turn=BLACK):
        """ Set up initial board configuration. """
        # Create the empty board array
        self.__pieces = [None] * 8
        for i in range(8):
            self.__pieces[i] = [0] * 8

        # Set up the initial 4 pieces
        self.__pieces[3][4] = WHITE
        self.__pieces[4][3] = WHITE
        self.__pieces[3][3] = BLACK
        self.__pieces[4][4] = BLACK

        # Current turn
        self.__turn = turn

        # Total number of flips because of a move
        self.__flips = 0

        # Configure heuristic functions for different agent types
        self.heuristics = dict()
        self.heuristics[AgentType.greedy] = self.get_current_player_count

    def clone(self):
        """
        Returns a copy of the current board
        :return: a copy of the current board
        """
        cloned = Board(self.__turn)
        for y in range(len(self.__pieces)):
            for x in range(len(self.__pieces[y])):
                cloned[x][y] = self[x][y]

        return cloned

    # Add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.__pieces[index]

    def get_turn(self):
        """ Get the current turn (-1 is black and 1 is white) """
        return self.__turn

    def change_turn(self):
        """ Change the current turn to the other color """
        # result_board = self.clone()
        # result_board.__turn = -result_board.__turn
        # return [(None, result_board)]
        self.__turn = -self.__turn

    def create_pass_successor(self):
        result_board = self.clone()
        result_board.__turn = -result_board.__turn
        return [(None, result_board)]

    def is_game_over(self):
        """ Check whether the game is over """
        return len(self.get_legal_moves(WHITE)) == 0 and len(self.get_legal_moves(BLACK)) == 0

    # ###def display(self, time):
    def __display(self):
        """" Display the board and the statistics of the ongoing game. """
        # ###print("    A B C D E F G H")
        # ###print("    ---------------")
        result = "    A B C D E F G H" + '\n'
        result += "    ---------------" + '\n'
        for y in range(7, -1, -1):
            # Print the row number
            # ###print(str(y + 1) + ' |', end=' ')
            result += str(y + 1) + ' | '
            for x in range(8):
                # Get the piece to print
                piece = self[x][y]
                if piece == -1:
                    # ###print("B", end=' ')
                    result += "B "
                elif piece == 1:
                    # ###print("W", end=' ')
                    result += "W "
                else:
                    # ###print(".", end=' ')
                    result += ". "
            # ###print('| ' + str(y + 1))
            result += '| ' + str(y + 1) + '\n'

        # ###print("    ---------------")
        # ###print("    A B C D E F G H\n")
        result += "    ---------------" + '\n'
        result += "    A B C D E F G H" + '\n'

        # ###print "STATISTICS (score / remaining time):"
        # ###print "Black: " + str(self.count(-1)) + ' / ' + str(time[-1])
        # ###print "White: " + str(self.count(1)) + ' / ' + str(time[1]) + '\n'
        # ###print("STATISTICS:")
        # ###print("-----------")
        # ###print("Black: {}".format(self.count(-1)))
        # ###print("White: {}".format(self.count(1)))
        # ###print("Current turn: {}".format(MyBoard.get_color_string(self.__turn)))
        # ---result += "STATISTICS:" + '\n'
        # ---result += "-----------" + '\n'
        # ---result += "Black: {}".format(self.count(-1)) + '\n'
        # ---result += "White: {}".format(self.count(1)) + '\n'
        # ---result += "Current turn: {}".format(MyBoard.get_color_string(self.__turn)) + '\n'

        return result

    def print_statistics(self):
        """
        Prints statistics: number of cells for each color, along with current turn
        """
        print("STATISTICS:")
        print("-----------")
        print("Black: {}".format(self.count(-1)))
        print("White: {}".format(self.count(1)))
        print("Current turn: {}".format(Board.get_color_string(self.__turn)))

    def __repr__(self):
        return str(self.__pieces)

    def __str__(self):
        """
        Return the string representation of the board
        :return: string representation of the board
        """
        return self.__display()
        # return str(self.__pieces)

    def count(self, color=10):
        """
        Count the number of pieces of the given color.
        :param color: 1 for white, -1 for black, 0 for empty spaces (If not specified, uses current turn)
        :return: number of cells associated with the specified color
        """
        count = 0

        # If color isn't specified, choose the current turn
        if color == 10:
            color = self.__turn

        for y in range(8):
            for x in range(8):
                if self[x][y] == color:
                    count += 1
        return count

    def get_final_score(self):
        """
        Get the final score of the two players; first one is for black, and second one is for white
        :return:
        """
        black_count = self.count(BLACK)
        white_count = self.count(WHITE)
        total = black_count + white_count
        if black_count == white_count:
            return black_count, white_count
        elif black_count > white_count:
            return black_count + 64 - total, white_count
        else:
            return black_count, white_count + 64 - total

    def get_squares(self, color=10):
        """
        Get the coordinates (x,y) for all pieces on the board of the given color.
        :param color: 1 for white, -1 for black, 0 for empty spaces (If not specified, uses current turn)
        :return: list of cell coordinates containing the specified color
        """
        squares = []

        # If color isn't specified, choose the current turn
        if color == 10:
            color = self.__turn

        for y in range(8):
            for x in range(8):
                if self[x][y] == color:
                    squares.append((x, y))
        return squares

    def get_successors(self, color=0):
        """
        Get the successor states from the current board
        :param color: color to do the move (If not specified uses current turn's color)
        :return: list of successor board states
        """

        if color == 0:
            color = self.__turn

        moves = self.get_legal_moves(color)
        result = []

        for move in moves:
            result.append((move, self.execute_move(move, color)))

        return result

    def get_legal_moves(self, color=0):
        """
        Return all the legal moves for the given color.
        :param color: 1 for white, -1 for black (If not specified, uses current turn)
        :return: list of legal moves for the specified color
        """

        # Store the legal moves
        moves = set()

        # If color isn't specified, choose the current turn
        if color == 0:
            color = self.__turn

        # Get all the squares with pieces of the given color.
        for square in self.get_squares(color):
            # Find all moves using these pieces as base squares.
            new_moves = self.get_moves_for_square(square)
            # Store these in the moves set.
            moves.update(new_moves)

        return list(moves)

    def get_moves_for_square(self, square):
        """
        Return all the legal moves that use the given square as a base
        square. That is, if the given square is (3,4) and it contains a black
        piece, and (3,5) and (3,6) contain white pieces, and (3,7) is empty,
        one of the returned moves is (3,7) because everything from there to
        (3,4) can be flipped.
        :param square: cell coordinates of the square we want to check
        :return: list of moves applicable to that square (considering the color)
        """
        (x, y) = square

        # Determine the color of the piece
        color = self[x][y]

        # Skip empty source squares
        if color == 0:
            return None

        # Search all possible directions
        moves = []
        for direction in self.__directions:
            move = self._discover_move(square, direction)
            if move:
                moves.append(move)
        # Return the generated list of moves
        return moves

    def execute_move(self, move, color=0):
        """
        Perform the given move on the board, and flips pieces as necessary.
        :param move: the move to be executed on the board
        :param color: 1 for white, -1 for black (If not specified, uses current turn)
        :return: a new board with the move applied to it
        """
        # Create a copy and apply the change to the copy
        result_board = self.clone()

        # If color isn't specified, choose the current turn
        if color == 0:
            color = self.__turn

        if move is not None:
            # Start at the new piece's square and follow it on all 8 directions
            # to look for pieces allowing flipping
            # Add the piece to the empty square
            flips = (flip for direction in self.__directions for flip in self._get_flips(move, direction, color))

            result_board.__flips = 0
            for x, y in flips:
                # ---self[x][y] = color
                original_color = result_board[x][y]
                result_board[x][y] = color

                # If the resulting color is different than the original color, count it as a flip
                if color != original_color:
                    result_board.__flips += 1

        # ---self.change_turn()
        result_board.change_turn()

        return result_board

    def _discover_move(self, origin, direction):
        """
        Return the endpoint of a legal move, starting at the given origin,
        and moving in the given direction.
        """
        x, y = origin
        color = int(self[x][y])
        flips = []

        # ###for x, y in Board._increment_move(origin, direction):
        for x, y in Board._increment_move(origin, direction):
            if self[x][y] == 0 and flips:
                return x, y
            elif self[x][y] == color or (self[x][y] == 0 and not flips):
                return None
            elif self[x][y] == -color:
                flips.append((x, y))

    def get_last_flip_count(self):
        """
        Get the number of flips caused by executing the last move on the board
        :return: number of flips caused by the move
        """
        return self.__flips

    def _get_flips(self, origin, direction, color):
        """
        Get the list of flips for a vertex and a direction to use within
        the execute_move function.
        :param origin: the cell to start
        :param direction: the direction to follow
        :param color: the color to check
        :return: total number of flips
        """

        # Initialize variable
        flips = [origin]

        # ###for x, y in Board._increment_move(origin, direction):
        for x, y in Board._increment_move(origin, direction):
            if self[x][y] == -color:
                flips.append((x, y))
            elif self[x][y] == 0 or (self[x][y] == color and len(flips) == 1):
                break
            elif self[x][y] == color and len(flips) > 1:
                return flips
        return []

    # ################# Functions used for heuristics ##########################

    def get_current_player_count(self):
        return self.count(self.__turn) - self.count(-self.__turn)

    # ##########################################################################

    @staticmethod
    def _increment_move(move, direction):
        """
        Generator expression for incrementing moves
        :param move: the move to consider
        :param direction: the direction to follow
        :return: moves in the specified direction
        """
        move = list(map(sum, list(zip(move, direction))))

        while all(list(map(lambda x: 0 <= x < 8, move))):
            yield move
            move = list(map(sum, list(zip(move, direction))))

    @staticmethod
    def get_col_char(col):
        """
        Convert 1, 2, etc. to 'a', 'b', etc.
        :param col: number corresponding to the desired column
        :return: the alphabetical representation of the specified column
        """
        return chr(ord('a') + col)

    @staticmethod
    def moves_string(moves):
        """
        Return the given list of coordinates as a nicely formatted list of
        moves. Example: [(2,3),(5,2)] -> 'c4, f3'
        :param moves: list of moves containing cell coordinates as tuples
        :return: formatted moves as a single comma-separated string
        """
        s = ""
        for i, move in enumerate(moves):
            if i == len(moves) - 1:
                s += Board.move_string(move)
            else:
                s += Board.move_string(move) + ', '
        return s

    @staticmethod
    def print_moves(moves):
        """ Print the list of coordinates. """
        print(Board.moves_string(moves))

    @staticmethod
    def move_string(move):
        """ Convert a numeric (x,y) coordinate like (2,3) into a piece name like 'c4'. """
        (x, y) = move
        return Board.get_col_char(x) + str(y + 1)

    @staticmethod
    def get_color_string(color):
        """
        Convert the specified integer color to its string representation
        :param color: integer value of the color (-1 for Black, 1 for White)
        :return: string representation of the specified color
        """
        return "Black" if color == BLACK else "White" if color == WHITE else "UNKNOWN"

