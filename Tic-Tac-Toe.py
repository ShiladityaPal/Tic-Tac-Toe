import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_SIZE = 3
SQUARE_SIZE = WIDTH // BOARD_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Fonts
font = pygame.font.Font(None, 50)

# Board
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Function to draw the Tic Tac Toe board
def draw_board():
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(screen, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)

# Function to draw the Xs and Os
def draw_xo():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 'X':
                draw_x(row, col)
            elif board[row][col] == 'O':
                draw_o(row, col)

# Function to draw an X at a specific position
def draw_x(row, col):
    x_offset = col * SQUARE_SIZE
    y_offset = row * SQUARE_SIZE
    pygame.draw.line(screen, RED, (x_offset, y_offset), (x_offset + SQUARE_SIZE, y_offset + SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, RED, (x_offset + SQUARE_SIZE, y_offset), (x_offset, y_offset + SQUARE_SIZE), LINE_WIDTH)

# Function to draw an O at a specific position
def draw_o(row, col):
    x_center = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y_center = row * SQUARE_SIZE + SQUARE_SIZE // 2
    radius = SQUARE_SIZE // 2 - LINE_WIDTH
    pygame.draw.circle(screen, BLUE, (x_center, y_center), radius, LINE_WIDTH)

# Function to check if a player has won
def check_winner(player):
    # Check rows and columns
    for i in range(BOARD_SIZE):
        if all(board[i][j] == player for j in range(BOARD_SIZE)) or all(board[j][i] == player for j in range(BOARD_SIZE)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(BOARD_SIZE)) or all(board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)):
        return True

    return False

# Function to check if the board is full
def is_board_full():
    return all(board[i][j] != ' ' for i in range(BOARD_SIZE) for j in range(BOARD_SIZE))

# Function to evaluate the current board state
def evaluate_board():
    if check_winner('X'):
        return -1
    elif check_winner('O'):
        return 1
    elif is_board_full():
        return 0
    else:
        return None

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, maximizing_player, alpha, beta):
    score = evaluate_board()

    if score is not None:
        return score

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Function to get the computer's move using minimax
def get_computer_move():
    best_score = float('-inf')
    best_move = None

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                move_score = minimax(board, 0, False, float('-inf'), float('inf'))
                board[i][j] = ' '

                if move_score > best_score:
                    best_score = move_score
                    best_move = (i, j)

    return best_move

# Main game loop
def main():
    player_turn = True  # True for 'X', False for 'O'
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over and player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE

                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    player_turn = not player_turn

            if not game_over and not player_turn:
                row, col = get_computer_move()
                board[row][col] = 'O'
                player_turn = not player_turn

        screen.fill(WHITE)
        draw_board()
        draw_xo()

        if check_winner('X'):
            game_over = True
            text = font.render("Player X wins!", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        elif check_winner('O'):
            game_over = True
            text = font.render("Player O wins!", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        elif is_board_full():
            game_over = True
            text = font.render("It's a tie!", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

if __name__ == "__main__":
    main()