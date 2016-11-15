from board import Board


def create_pass_configuration_board() -> Board:
    """
    Creates a board with a configuration such that the current turn (white) has to pass
    :return: a board with pass configuration
    """
    board = Board(turn=1)

    # #######################
    # Test board for pass using this video:
    # https://youtu.be/fZfUd3utD5w?t=323
    # Column 0
    board[0][1] = -1
    board[0][2] = -1
    board[0][3] = -1
    board[0][4] = -1
    board[0][5] = -1
    board[0][6] = -1
    board[0][7] = -1
    # Column 1
    board[1][3] = -1
    board[1][4] = -1
    board[1][5] = -1
    board[1][6] = -1
    board[1][7] = -1
    # Column 2
    board[2][3] = 1
    board[2][4] = -1
    board[2][5] = -1
    board[2][6] = 1
    board[2][7] = -1
    # Column 3
    board[3][3] = 1
    board[3][4] = 1
    board[3][5] = -1
    board[3][6] = -1
    board[3][7] = -1
    # Column 4
    board[4][3] = 1
    board[4][4] = 1
    board[4][5] = -1
    board[4][6] = -1
    board[4][7] = -1
    # Column 5
    board[5][3] = 1
    board[5][4] = -1
    board[5][5] = 1
    board[5][6] = 1
    board[5][7] = -1
    # Column 6
    board[6][3] = 1
    board[6][4] = 1
    board[6][5] = 1
    board[6][7] = -1
    # Column 7
    board[7][3] = 1
    # #######################

    return board
