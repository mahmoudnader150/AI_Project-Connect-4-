class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [['-' for _ in range(cols)] for _ in range(rows)]

    def display(self):
        for row in self.board:
            for cell in row:
                print(cell, end=' ')
            print()

    def drop_piece(self, col, piece):
        for row in range(self.rows-1, -1, -1):
            if self.board[row][col] == '-':
                self.board[row][col] = piece
                return True
        return False

    def is_full(self):
        for col in range(self.cols):
            if self.board[0][col] == '-':
                return False
        return True

    def is_winner(self, piece):
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.cols-3):
                if self.board[row][col] == piece and \
                    self.board[row][col+1] == piece and \
                    self.board[row][col+2] == piece and \
                    self.board[row][col+3] == piece:
                    return True

        # Check vertical
        for row in range(self.rows-3):
            for col in range(self.cols):
                if self.board[row][col] == piece and \
                    self.board[row+1][col] == piece and \
                    self.board[row+2][col] == piece and \
                    self.board[row+3][col] == piece:
                    return True

        # Check diagonal (down-right)
        for row in range(self.rows-3):
            for col in range(self.cols-3):
                if self.board[row][col] == piece and \
                    self.board[row+1][col+1] == piece and \
                    self.board[row+2][col+2] == piece and \
                    self.board[row+3][col+3] == piece:
                    return True

        # Check diagonal (up-right)
        for row in range(3, self.rows):
            for col in range(self.cols-3):
                if self.board[row][col] == piece and \
                    self.board[row-1][col+1] == piece and \
                    self.board[row-2][col+2] == piece and \
                    self.board[row-3][col+3] == piece:
                    return True

        return False
    
def main():
        # Initialize the board
    board = Board(6, 7)

    # Initialize the players
    players = ['X', 'O']
    current_player = 0

    # Play the game
    while not board.is_full():
        # Display the board
        board.display()

        # Get the current player's move
        col = int(
            input(f"Player {players[current_player]} enter column (0-6): "))

        # Make the move
        if not board.drop_piece(col, players[current_player]):
            print("Column is full, try again.")
            continue

        # Check for a win
        if board.is_winner(players[current_player]):
            print(f"Player {players[current_player]} wins!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % 2

    # Display the final state of the board
    board.display()


if __name__ == '__main__':
    main()

