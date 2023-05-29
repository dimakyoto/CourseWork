from InterfaceElements import *

# Screen size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Fonts
Instruction_font = pygame.font.SysFont("timesnewroman", 24)
ButtonFont = pygame.font.SysFont("timesnewroman", 18)

# Program title
pygame.display.set_caption("THE SHORTEST PATH IN THE MAZE")

# FPS
FPS = 60
CLOCK = pygame.time.Clock()

# Open the result file before the loop
result_file = open("search_results.txt", "w")

# Interface
PADDING = 32
board_height = HEIGHT - 3.5 * PADDING
board_width = WIDTH - 3.5 * PADDING
board_start = (PADDING, PADDING)

# Max length of input new maze size
MAX_LENGTH = 15

# Color dictionary
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
    "yellow": (255, 255, 0),  # button color change when it's clicked
    "lightcoral": (240, 128, 128),  # for maze generation
    "blue": (0, 0, 255),  # active
    "deepskyblue": (0, 191, 255),  # inactive
    "gainsboro": (220, 220, 220),  # maze size interface filling
}

# TextFields complexity results
Comparisons = TextField(x=520, y=32, width=250, height=37.5)
Iterations = TextField(x=520, y=69, width=250, height=37.5)
Visited_cells = TextField(x=520, y=106, width=250, height=37.5)
Execution_time = TextField(x=520, y=143, width=250, height=37.5)

# Input line for size changing
input_line = pygame.Rect(300, 300, 100, 32)

# Buttons
start_button = Button(
    horizontal=PADDING, vertical=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Search Start", textcolor=colors["black"],
    button_color=colors["green"], screen=screen, font=ButtonFont)

maze_button = Button(
    horizontal=4.7 * PADDING, vertical=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Maze", textcolor=colors["black"],
    button_color=colors["white"], screen=screen, font=ButtonFont)

maze_size_button = Button(
    horizontal=8.3 * PADDING, vertical=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Size", textcolor=colors["black"],
    button_color=colors["white"], screen=screen, font=ButtonFont)

reset_button = Button(
    horizontal=12 * PADDING, vertical=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Reset", textcolor=colors["black"],
    button_color=colors["crimson"], screen=screen, font=ButtonFont)

dijkstra_button = Button(
    horizontal=18.5 * PADDING, vertical=7 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Dijkstra", textcolor=colors["black"],
    button_color=colors["white"], screen=screen, font=ButtonFont)

astar_man_button = Button(
    horizontal=18.5 * PADDING, vertical=10 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="A* (man)", textcolor=colors["black"],
    button_color=colors["white"], screen=screen, font=ButtonFont)

astar_evk_button = Button(
    horizontal=18.5 * PADDING, vertical=13 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="A* (evk)", textcolor=colors["black"],
    button_color=colors["white"], screen=screen, font=ButtonFont)

back_button = Button(
    horizontal=11 * PADDING, vertical=HEIGHT - 7.5 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Back", textcolor=colors["black"],
    button_color=colors["crimson"], screen=screen, font=ButtonFont)
