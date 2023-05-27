from ShowElements import *
import pygame

pygame.init()

# Screen size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Fonts
Instruction_font = pygame.font.SysFont("timesnewroman", 24)
RectButtonFont = pygame.font.SysFont("timesnewroman", 18)

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

# Complexity results
Comparisons = TextField(x=520, y=32, width=250, height=37.5)
Iterations = TextField(x=520, y=69, width=250, height=37.5)
Visited_cells = TextField(x=520, y=106, width=250, height=37.5)
Execution_time = TextField(x=520, y=143, width=250, height=37.5)

# Input line for size changing
input_line = pygame.Rect(300, 300, 100, 32)

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
    "gainsboro": (220, 220, 220),  # maze size filling
}

# Buttons
start_button = RectButton(
    left=PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height= 1.5 * PADDING,
    text="Search Start", textcolor=colors["black"],
    rectcolor=colors["green"], screen=screen, font=RectButtonFont)

maze_button = RectButton(
    left=4.5 * PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height= 1.5 * PADDING,
    text="Maze", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

maze_size_button = RectButton(
    left=8 * PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Size", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

draw_button = RectButton(
    left=11.5 * PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Draw Wall", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

erase_button = RectButton(
    left=15 * PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Erase Wall", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

reset_button = RectButton(
    left=18.5 * PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Reset", textcolor=colors["black"],
    rectcolor=colors["crimson"], screen=screen, font=RectButtonFont)

dijkstra_button = RectButton(
    left=18.5 * PADDING, top=7 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Dijkstra", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

astar_man_button = RectButton(
    left=18.5 * PADDING, top=10 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="A* (man)", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

astar_evk_button = RectButton(
    left=18.5 * PADDING, top=13 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="A* (evk)", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

back_button = RectButton(
    left=11 * PADDING, top=HEIGHT - 7.5 * PADDING,
    width=3 * PADDING, height=1.5 * PADDING,
    text="Back", textcolor=colors["black"],
    rectcolor=colors["crimson"], screen=screen, font=RectButtonFont)
