from board import Board
import time
import random
import numpy as np
import main as mn
import math

# GAME LINK
# http://kevinshannon.com/connect4/

ROW_COUNT = 6
COLUMN_COUNT = 7

BOARD = np.zeros((ROW_COUNT, COLUMN_COUNT))


def main():
    board = Board()

    time.sleep(2)
    game_end = False
    while not game_end:
        (game_board, game_end) = board.get_game_grid()

        # FOR DEBUG PURPOSES
        board.print_grid(game_board)

        # YOUR CODE GOES HERE

        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                if(game_board[r][c] == 0):
                    BOARD[r, c] = 0
                if(game_board[r][c] == 1):
                    BOARD[r, c] = 1
                if(game_board[r][c] == 2):
                    BOARD[r, c] = 2

        print(BOARD)

        # Insert here the action you want to perform based on the output of the algorithm
        # You can use the following function to select a column
        # col, minimax_score = mn.minimax(BOARD, 3, -math.inf, math.inf, True)
        col, minimax_score = mn.minimax(BOARD, 5, -math.inf, math.inf, True)

        if mn.is_valid_location(BOARD, col):
            # delay time
            row = mn.get_next_open_row(BOARD, col)
            mn.drop_piece(BOARD, row, col, 2)
            if mn.winning_move(BOARD, 2):
                game_over = True

        print(col)
        board.select_column(col)
        print(BOARD)
        time.sleep(2)
        if mn.winning_move(BOARD, 1) or mn.winning_move(BOARD, 2):
            break
        game_end = mn.is_terminal_nade(BOARD)


if __name__ == "__main__":
    main()
def choose_depth():
    root = tk.Tk()
    root.title("Connect Four Depth Selection")

    def set_depth(value):
        nonlocal depth
        depth = int(value)

    depth = 2

    def start_game():
        nonlocal root
        root.destroy()

    tk.Label(root, text="Select Depth:").pack()

    depth_var = tk.StringVar(root, value=str(depth))
    depth_scale = tk.Scale(root, from_=2, to=6,
                           orient=tk.HORIZONTAL, variable=depth_var)
    depth_scale.pack()

    start_button = tk.Button(root, text="Start Game", command=start_game)
    start_button.pack()

    root.mainloop()

    return depth


if __name__ == "__main__":
    main()
