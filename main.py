import pygame


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


class BoardGUI:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size
        self.height = (rows + 1) * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Connect Four")

        self.board = Board(rows, cols)
        self.players = ['1', '2']
        self.current_player = 0

        self.font = pygame.font.SysFont(None, 48)

    def draw_board(self):
        self.screen.fill((0, 0, 255))

        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size
                y = (row + 1) * self.cell_size
                pygame.draw.circle(self.screen, (0, 0, 0), (
                    x + self.cell_size // 2, y + self.cell_size // 2), self.cell_size // 2 - 4, 4)
                if self.board.board[row][col] == '1':
                    pygame.draw.circle(self.screen, (255, 0, 0), (
                        x + self.cell_size // 2, y + self.cell_size // 2), self.cell_size // 2 - 8)
                elif self.board.board[row][col] == '2':
                    pygame.draw.circle(self.screen, (255, 255, 0), (
                        x + self.cell_size // 2, y + self.cell_size // 2), self.cell_size // 2 - 8)

        pygame.display.update()

    def get_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // self.cell_size
                    if self.board.drop_piece(col, self.players[self.current_player]):
                        return

            self.draw_board()
            text = self.font.render(
                f"Player {self.players[self.current_player]}'s turn", True, (255, 255, 255))
            self.screen.blit(
                text, (self.width // 2 - text.get_width() // 2, 10))
            pygame.display.update()

    def play(self):
        while not self.board.is_full():
            self.get_input()

            if self.board.is_winner(self.players[self.current_player]):
                self.draw_board()
                text = self.font.render(
                    f"Player {self.players[self.current_player]} wins!", True, (255, 255, 255))
                self.screen.blit(
                    text, (self.width // 2 - text.get_width() // 2, 10))
                pygame.display.update()
                pygame.time.delay(3000)
                return

            self.current_player = (self.current_player + 1) % 2

        self.draw_board()
        text = self.font.render("Game over!", True, (255, 255, 255))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, 10))
        pygame.display.update()
        pygame.time.delay(3000)


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
    pygame.init()

    board_gui = BoardGUI(6, 7, 80)
    board_gui.play()

    pygame.quit()
