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

# Відкриття файлу перед циклом
result_file = open("search_results.txt", "w")

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

#  Кнопки
start_button = RectButton(
    left=PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Search Start", textcolor=colors["black"],
    rectcolor=colors["green"], screen=screen, font=RectButtonFont)

maze_button = RectButton(
    left=4.5 * PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Maze", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

draw_button = RectButton(
    left=8 * PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Draw Wall", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

erase_button = RectButton(
    left=11.5 * PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Erase Wall", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

reset_button = RectButton(
    left=15 * PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Reset", textcolor=colors["black"],
    rectcolor=colors["crimson"], screen=screen, font=RectButtonFont)

dijkstra_button = RectButton(
    left=17 * PADDING, top=3 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Dijkstra", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

astar_man_button = RectButton(
    left=17 * PADDING, top=6 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="A* (man)", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

astar_evk_button = RectButton(
    left=17 * PADDING, top=9 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="A* (evk)", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

