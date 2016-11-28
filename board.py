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
EMPTY = 0


class Board:
    # List of all 8 directions on the board, as (x,y) offsets
    __directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

    def __init__(self, turn=BLACK):
        """ Set up initial board configuration. """
        # Create the empty board array
        self.__pieces = [None] * 8
        for i in range(8):
            self.__pieces[i] = [EMPTY] * 8

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
        self.heuristics[AgentType.greedy] = self.get_last_flip_count
        self.heuristics[AgentType.simple] = self.get_token_difference
        self.heuristics[AgentType.composite] = self.composite_heuristic
        self.heuristics[AgentType.mobile] = self.mobile_greedy
        self.heuristics[AgentType.corner] = self.greedy_corner

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

    def get_last_flip_count(self):
        """
        Get the number of flips caused by executing the last move on the board
        :return: number of flips caused by the move
        """
        return self.__flips

    def get_token_difference(self):
        """
        Get the difference between the tokens between the current player and the opponent
        :return: difference between the tokens in the board
        """
        return self.count(self.__turn) - self.count(-self.__turn)

    # Code for heuristic from here: https://kartikkukreja.wordpress.com/2013/03/30/heuristic-function-for-reversiothello/
    def composite_heuristic(self):
        v = [[None] * 8] * 8
        v[0] = [20, -3, 11, 8, 8, 11, -3, 20]
        v[1] = [-3, -7, -4, 1, 1, -4, -7, -3]
        v[2] = [11, -4, 2, 2, 2, 2, -4, 11]
        v[3] = [8, 1, 2, -3, -3, 2, 1, 8]
        v[4] = [8, 1, 2, -3, -3, 2, 1, 8]
        v[5] = [11, -4, 2, 2, 2, 2, -4, 11]
        v[6] = [-3, -7, -4, 1, 1, -4, -7, -3]
        v[7] = [20, -3, 11, 8, 8, 11, -3, 20]

        my_tiles = 0
        opponent_tiles = 0
        my_front_tiles = 0
        opponent_front_tiles = 0
        p = 0.0
        c = 0.0
        l = 0.0
        m = 0.0
        f = 0.0
        d = 0.0

        for i in range(8):
            for j in range(8):
                if self[i][j] == self.__turn:
                    d += v[i][j]
                    my_tiles += 1
                elif self[i][j] == -self.__turn:
                    d -= v[i][j]
                    opponent_tiles += 1

                if self[i][j] != EMPTY:
                    for direction in self.__directions:
                        x_neighbor, y_neighbor = map(sum, zip((i, j), direction))
                        if 0 <= x_neighbor < 8 and 0 <= y_neighbor < 8 and self[x_neighbor][y_neighbor] == EMPTY:
                            if self[i][j] == self.__turn:
                                my_tiles += 1
                            elif self[i][j] == -self.__turn:
                                opponent_tiles += 1
                            break

        if my_tiles > opponent_tiles:
            p = (100.0 * my_tiles) / (my_tiles + opponent_tiles)
        elif my_tiles < opponent_tiles:
            p = -(100.0 * my_tiles) / (my_tiles + opponent_tiles)
        else:
            p = 0

        if my_front_tiles > opponent_front_tiles:
            f = -(100.0 * my_front_tiles) / (my_front_tiles + opponent_front_tiles)
        elif my_front_tiles < opponent_front_tiles:
            f = (100.0 * my_front_tiles) / (my_front_tiles + opponent_front_tiles)
        else:
            f = 0

        # Corner occupancy
        my_tiles = 0
        opponent_tiles = 0

        if self[0][0] == self.__turn:
            my_tiles += 1
        elif self[0][0] == -self.__turn:
            opponent_tiles += 1

        if self[0][7] == self.__turn:
            my_tiles += 1
        elif self[0][7] == -self.__turn:
            opponent_tiles += 1

        if self[7][0] == self.__turn:
            my_tiles += 1
        elif self[7][0] == -self.__turn:
            opponent_tiles += 1

        if self[7][7] == self.__turn:
            my_tiles += 1
        elif self[7][7] == -self.__turn:
            opponent_tiles += 1

        c = 25 * (my_tiles - opponent_tiles)

        # Corner closeness
        my_tiles = 0
        opponent_tiles = 0

        if self[0][0] == EMPTY:
            if self[0][1] == self.__turn:
                my_tiles += 1
            elif self[0][1] == -self.__turn:
                opponent_tiles += 1
            if self[1][1] == self.__turn:
                my_tiles += 1
            elif self[1][1] == -self.__turn:
                opponent_tiles += 1
            if self[1][0] == self.__turn:
                my_tiles += 1
            elif self[1][0] == -self.__turn:
                opponent_tiles += 1

        if self[0][7] == EMPTY:
            if self[0][6] == self.__turn:
                my_tiles += 1
            elif self[0][6] == -self.__turn:
                opponent_tiles += 1
            if self[1][6] == self.__turn:
                my_tiles += 1
            elif self[1][6] == -self.__turn:
                opponent_tiles += 1
            if self[1][7] == self.__turn:
                my_tiles += 1
            elif self[1][7] == -self.__turn:
                opponent_tiles += 1

        if self[7][0] == EMPTY:
            if self[7][1] == self.__turn:
                my_tiles += 1
            elif self[7][1] == -self.__turn:
                opponent_tiles += 1
            if self[6][1] == self.__turn:
                my_tiles += 1
            elif self[6][1] == -self.__turn:
                opponent_tiles += 1
            if self[6][0] == self.__turn:
                my_tiles += 1
            elif self[6][0] == -self.__turn:
                opponent_tiles += 1

        if self[7][7] == EMPTY:
            if self[6][7] == self.__turn:
                my_tiles += 1
            elif self[6][7] == -self.__turn:
                opponent_tiles += 1
            if self[6][6] == self.__turn:
                my_tiles += 1
            elif self[6][6] == -self.__turn:
                opponent_tiles += 1
            if self[7][6] == self.__turn:
                my_tiles += 1
            elif self[7][6] == -self.__turn:
                opponent_tiles += 1

        l = -12.5 * (my_tiles - opponent_tiles)

        # Mobility
        my_tiles = len(self.get_legal_moves(self.__turn))
        opponent_tiles = len(self.get_legal_moves(-self.__turn))

        if my_tiles > opponent_tiles:
            m = (100.0 * my_tiles) / (my_tiles + opponent_tiles)
        elif my_tiles < opponent_tiles:
            m = -(100.0 * my_tiles) / (my_tiles + opponent_tiles)
        else:
            m = 0

        # Final weighted score
        return (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)

    # ##########################################################################

    def mobile_greedy(self):
        """
        This corner mixes the greedy approach with a relatively low weight and a higher weight
        on the mobility heuristic.
        """
        return 10 * self.get_token_difference() + 42 * self.mobility()

    def greedy_corner(self):
        """
        This corner mixes the greedy approach with a low weight and a high weight
        on the corner heuristic.
        """
        return 10 * self.get_token_difference() + 801 * self.corner_occupancy()

    def mobility(self):
        """
        This heuristic aims to calculate the respective contrast between the moves from the
        max player with the min player.
        The purpose of this heuristic is to restrict the adversary mobility
        and expand its own mobility.
        """
        # Get my moves
        my_moves = len(self.get_legal_moves(self.__turn))
        opponent_moves = len(self.get_legal_moves(-self.__turn))

        if my_moves > opponent_moves:
            return (100 * my_moves) / (my_moves + opponent_moves)
        elif my_moves < opponent_moves:
            return (-100 * opponent_moves) / (my_moves + opponent_moves)
        else:
            return 0

    def corner_occupancy(self):
        """
        The corners of the othello board have a high value, i.e. the token cannot be flipped,
        and they allow a player to place tokens around them and provide stability to the player’s token.
        Effectively giving the player a higher chance to win.
        This heuristic simply establishes a score on them based on the adversary and the current players
        token that are in the corners.
        """
        my_tiles = 0
        opponent_tiles = 0
        if self[0][0] == self.__turn:
            my_tiles += 1
        elif self[0][0] == -self.__turn:
            opponent_tiles += 1

        if self[0][7] == self.__turn:
            my_tiles += 1
        elif self[0][7] == -self.__turn:
            opponent_tiles += 1

        if self[7][0] == self.__turn:
            my_tiles += 1
        elif self[7][0] == -self.__turn:
            opponent_tiles += 1

        if self[7][7] == self.__turn:
            my_tiles += 1
        elif self[7][7] == -self.__turn:
            opponent_tiles += 1

        # Here we multiply by 25 the score to give a special emphasis on the
        # corners.
        return 25 * (my_tiles - opponent_tiles)

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

