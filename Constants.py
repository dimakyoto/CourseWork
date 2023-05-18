import pygame.time
from Maze import *
from ShowElements import *
pygame.init()

# Розмір екрану
WIDTH, HEIGHT = 650, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Шрифт кнопок
RectButtonFont = pygame.font.SysFont("timesnewroman", 18)

# Назва проги
pygame.display.set_caption("THE SHORTEST PATH IN THE MAZE")

# FPS
FPS = 60
CLOCK = pygame.time.Clock()

# Інтерфейс
PADDING = 32
board_height = HEIGHT - 3.5 * PADDING
board_width = WIDTH - 3.5 * PADDING
v_cells = 30
h_cells = 30
cell_size = int(min(board_height / (v_cells), board_width / (h_cells)))
board_start = (PADDING, PADDING)

# Словник для кольорів
colors = {
    "black": (0, 0, 0),  # background
    "snow": (250, 250, 250),  # routes in maze
    "white": (255, 255, 255),  # buttons
    "darkgreen": (0, 100, 0),  # start target
    "crimson": (220, 20, 60),  # finish target
    "lightslategray": (119, 136, 153),  # walls in maze
    "lime": (0, 255, 0),  # explored
    "green": (0, 255, 127),  # start button
    "gold": (255, 215, 0),  # shortest path
    "yellow": (255, 255, 0),  # button color change when its clicked
    "lightcoral": (240, 128, 128)  # for maze generation
}

# Змінні константи для мейн-циклу
RUNNING = True
FREEZETIME = 0.1
SEARCH = False
DRAW = False
ERASE = False
RESET = False
ALGO = None
PRESS = False
board = Board(v_cells, h_cells, board_start[0], board_start[1], cell_size, screen, colors)


