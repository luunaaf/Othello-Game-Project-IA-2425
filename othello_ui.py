import pygame
import sys
import numpy as np
from othello_game import OthelloGame
from mcts import uct_search

pygame.init()

TILE_SIZE = 80
BOARD_SIZE = 8
WIDTH = TILE_SIZE * BOARD_SIZE
HEIGHT = TILE_SIZE * BOARD_SIZE + 40 
FONT = pygame.font.SysFont("arial", 24)

LIGHT_PINK = (250, 220, 228)
LIGHT_BLUE = (157, 210, 219)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOARD_BG = (204, 255, 255)
GRID_COLOR = (188, 188, 188)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello by Estrella & Loubna")

game = OthelloGame()
state = game.get_initial_state()

human_color = 1  # Blanco
ai_color = 2     # Azul
current_player = 1

history = []  

def print_board(state):
    symbols = {0: '0', 1: '1', 2: '2'}  
    for row in state:
        print(' '.join(symbols[cell] for cell in row))
    print()

def draw_board():
    screen.fill(BOARD_BG)
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + 40, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, LIGHT_PINK, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

            value = state[y][x]
            if value == 1:
                pygame.draw.circle(screen, WHITE, rect.center, TILE_SIZE // 2 - 5)
            elif value == 2:
                pygame.draw.circle(screen, LIGHT_BLUE, rect.center, TILE_SIZE // 2 - 5)

    white_count = np.sum(state == 1)
    black_count = np.sum(state == 2)
    counter_text = FONT.render(f"Blancas: {white_count}   Azules: {black_count}", True, BLACK)
    screen.blit(counter_text, (10, 5))

def show_winner():
    white_count = np.sum(state == 1)
    black_count = np.sum(state == 2)
    if white_count > black_count:
        msg = "GANASTE TÚ"
    elif black_count > white_count:
        msg = "GANÓ LA IA" 
    else:
        msg = "EMPATE "

    text = FONT.render(msg, True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(5000)
    pygame.quit()
    sys.exit()

while True:
    draw_board()
    pygame.display.flip()

    if game.is_terminal(state):
        white_count = np.sum(state == 1)
        black_count = np.sum(state == 2)

        if white_count > black_count:
            winner = 1
        elif black_count > white_count:
            winner = 2
        else:
            winner = 0  

        print("\n== RESULTADOS DE LA PARTIDA ==")
        for idx, (s, p) in enumerate(history):
            label = 1 if winner == p else -1 if winner != 0 and winner != p else 0
            print(f"Turno {idx+1} - Jugador {p} - Resultado: {label}")
            print_board(s)

        show_winner()
    legal_moves = game.get_legal_moves(state, current_player)
    if not legal_moves:
        print(f"Jugador {current_player} no tiene movimientos válidos. Pasa turno.")
        current_player = 3 - current_player
        continue

    if current_player == ai_color:
        move = uct_search(state, ai_color, budget=100, cp=1.4)
        if move is not None:
            state = game.next_state(state, move, ai_color)
            print(f"[IA] Jugador {ai_color} movió a {move}")
            print_board(state)
            history.append((state.copy(), ai_color))
        current_player = human_color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and current_player == human_color:
            mx, my = pygame.mouse.get_pos()
            grid_x = mx // TILE_SIZE
            grid_y = (my - 40) // TILE_SIZE

            move = (grid_y, grid_x)
            if move in game.get_legal_moves(state, human_color):
                state = game.next_state(state, move, human_color)
                print(f"[HUMANO] Jugador {human_color} movió a {move}")
                print_board(state)
                history.append((state.copy(), human_color))
                current_player = ai_color
