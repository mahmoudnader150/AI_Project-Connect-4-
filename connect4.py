import numpy as np
import pygame
import sys
import math
import random

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


EMPTY = 0

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

WINDOW_LENGTH = 4
PLAYER_PIECE = 1
AI_PIECE = 2
# create 2D array with zeroes


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


# valid to put the piece
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


# flip the board (bl3ks)
def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # check horizontal locations
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # check horizontal locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # positive diagonls
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # negative diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    # center column score
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count*3

    # horizontal score
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # vertical score
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # positive slope
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Negative Slope
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


# terminal node when the game ends
def is_terminal_nade(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# minimax fuction


def minimax(board, depth, alpha, beta, maximizingplayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_nade(board)
    # base case
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 1000000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -1000000000000000)
            else:  # game is over
                return (None, 0)
        else:  # depth is zero
            return (None, score_position(board, AI_PIECE))

    # False and True in parameters is for switching between minimizing and maximizing playes.....
    if maximizingplayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if(alpha >= beta):
                break
        return column, value

    else:  # Minimizing Player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_valid_locations(board):
    valid_locations = []
    # collect all valid possible moves
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


# get best move by from all possibilities
def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        # count score of new simulated board
        score = score_position(temp_board, piece)
        # Maximize on best col according to score ...
        if(score > best_score):
            best_score = score
            best_col = col

    return best_col


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(
                screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2),   int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # color cell depending on value
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(
                    screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(
                    screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    # update screen after changes
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False


# start screen
pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE  # additional row for the dropping piece

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)   # radius of circles

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()


FONT = pygame.font.SysFont("arial.ttf", 80)

turn = random.randint(PLAYER, AI)
# while game not ende
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # event for mouse motion
        if event.type == pygame.MOUSEMOTION:
            # delete circles
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(
                    screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()
        # mouse button down event
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Move tile after win
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # Player 1 input
            if turn == PLAYER:
                # dimensions of piece equation
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = FONT.render("Player 1 WINS !!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                turn += 1
                turn = turn % 2

                print_board(board)
                draw_board(board)

    # ai turn
    if turn == AI and not game_over:

        #col = random.randint(0, COLUMN_COUNT-1)
        #col = pick_best_move(board, AI_PIECE)
        col, minimax_score = minimax(board, 4, -math.inf, math.inf, True)
        if is_valid_location(board, col):
            # delay time
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = FONT.render("Computer WINS !!!", 2, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            # exchang turns
            turn += 1
            turn = turn % 2

            print_board(board)
            draw_board(board)

    if game_over:
        pygame.time.wait(3000)
