import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7
# create 2D array with zeroes


def create_board():
    board = np.zeros((6, 7))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


# valid to put the piece
def is_valid_location(board, col):
    return board[5][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


# flip the board (bl3ks)
def print_board(board):
    print(np.flip(board, 0))


board = create_board()
print_board(board)
game_over = False
turn = 0

# while game not ende
while not game_over:
    # Player 1 input
    if turn == 0:
        col = int(input("Player 1 Choose your column(0-6):"))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

    # Player 2 input
    else:
        col = int(input("Player 2 Choose your column(0-6):"))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

    print_board(board)
    # exchang turns
    turn += 1
    turn = turn % 2
