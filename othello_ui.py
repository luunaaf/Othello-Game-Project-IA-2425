import pygame
import sys

pygame.init()

TILE_SIZE = 120
BOARD_SIZE = 8
WIDTH = HEIGHT = TILE_SIZE * BOARD_SIZE

LIGHT_PINK = (250, 220, 228)
LIGHT_BLUE = (157, 210, 219)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOARD_BG = (204, 255, 255)
GRID_COLOR = (188, 188, 188)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello By Estrella and Loubna")

board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

board[3][3] = "white"
board[3][4] = "black"
board[4][3] = "black"
board[4][4] = "white"

def draw_board():
    screen.fill(BOARD_BG)
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, LIGHT_PINK, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

            if board[y][x] == "white":
                pygame.draw.circle(screen, WHITE, rect.center, TILE_SIZE // 2 - 5)
            elif board[y][x] == "black":
                pygame.draw.circle(screen, LIGHT_BLUE, rect.center, TILE_SIZE // 2 - 5)

current_player = "black"

while True:
    draw_board()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            grid_x = mx // TILE_SIZE
            grid_y = my // TILE_SIZE

            if board[grid_y][grid_x] is None:
                board[grid_y][grid_x] = current_player
                current_player = "white" if current_player == "black" else "black"
