import pygame
import sys

# ---------------- SETTINGS ----------------
ROWS = 6
COLS = 7
SQUARESIZE = 100
RADIUS = SQUARESIZE // 2 - 8

WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE

# Colors
BLACK = (20, 20, 20)
YELLOW = (255, 215, 0)
RED = (255, 50, 50)
BLUE = (50, 120, 255)
WHITE = (255, 255, 255)

# ---------------- BOARD ----------------
def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

board = create_board()

def is_valid(col):
    return board[ROWS - 1][col] == 0

def next_row(col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def drop_piece(row, col, piece):
    board[row][col] = piece

def winning_move(piece):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Positive diagonal
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Negative diagonal
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

# ---------------- DRAW BOARD ----------------
def draw_board(screen):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(
                screen,
                YELLOW,
                (c*SQUARESIZE, (r+1)*SQUARESIZE, SQUARESIZE, SQUARESIZE)
            )

            pygame.draw.circle(
                screen,
                BLACK,
                (c*SQUARESIZE + SQUARESIZE//2,
                 (r+1)*SQUARESIZE + SQUARESIZE//2),
                RADIUS
            )

    # Draw pieces
    for c in range(COLS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(
                    screen, RED,
                    (c*SQUARESIZE + SQUARESIZE//2,
                     HEIGHT - (r*SQUARESIZE + SQUARESIZE//2)),
                    RADIUS
                )
            elif board[r][c] == 2:
                pygame.draw.circle(
                    screen, BLUE,
                    (c*SQUARESIZE + SQUARESIZE//2,
                     HEIGHT - (r*SQUARESIZE + SQUARESIZE//2)),
                    RADIUS
                )

    pygame.display.update()

# ---------------- HOW TO PLAY SCREEN ----------------
def show_instructions(screen, font):
    screen.fill(BLACK)

    lines = [
        "CONNECT FOUR - HOW TO PLAY",
        "1. Two players take turns.",
        "2. Move mouse and click a column.",
        "3. Piece will drop automatically.",
        "4. Connect 4 pieces to win.",
        " ",
        "CLICK ANYWHERE TO START"
    ]

    y = 100
    for text in lines:
        label = font.render(text, True, WHITE)
        screen.blit(label, (50, y))
        y += 60

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# ---------------- MAIN GAME ----------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Four")
font = pygame.font.SysFont("arial", 40)

show_instructions(screen, font)

turn = 0
game_over = False

draw_board(screen)

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse hover
        if event.type == pygame.MOUSEMOTION and not game_over:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
            xpos = event.pos[0]

            color = RED if turn == 0 else BLUE
            pygame.draw.circle(screen, color, (xpos, SQUARESIZE//2), RADIUS)
            pygame.display.update()

        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))

            col = event.pos[0] // SQUARESIZE

            if is_valid(col):
                row = next_row(col)
                piece = 1 if turn == 0 else 2
                drop_piece(row, col, piece)

                if winning_move(piece):
                    text = f"Player {piece} Wins!"
                    label = font.render(text, True,
                                        RED if piece == 1 else BLUE)
                    screen.blit(label, (40, 10))
                    game_over = True

                draw_board(screen)
                turn = (turn + 1) % 2

                if game_over:
                    pygame.time.wait(3000)
                    pygame.quit()
                    sys.exit()
