import random
import time
from Constants import *


class Board:
    """
    This class allows representing and displaying the state of the board,
    including the placement of walls, visited and passable cells, the start and target cells.
    It also provides methods to get neighboring cells and reset the board to its initial state.
    """
    def __init__(self, v_cells: int, h_cells: int, origin_x: int, origin_y: int,
                 cell_size: int, screen: pygame):
        self.v_cells = v_cells
        self.h_cells = h_cells
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.cell_size = cell_size
        self.screen = screen

        self.wall = set()
        self.visited = set()
        self.frontiers = set()
        self.path = list()
        self.start = None
        self.target = None

    def draw_board(self, return_cells=True):
        cells = []
        for i in range(self.v_cells):
            row = []
            for j in range(self.h_cells):
                rect = pygame.Rect(self.origin_x + i * self.cell_size,
                                   self.origin_y + j * self.cell_size,
                                   self.cell_size, self.cell_size)
                color = colors["snow"]
                if (i, j) == self.start:
                    color = colors["darkgreen"]
                elif (i, j) == self.target:
                    color = colors["crimson"]
                elif (i, j) in self.frontiers:
                    color = colors["lightcoral"]
                elif (i, j) in self.wall:
                    color = colors["lightslategray"]
                elif (i, j) in self.path:
                    color = colors["gold"]
                else:
                    for node in self.visited:
                        if (i, j) == node.state:
                            color = colors["lime"]
                pygame.draw.rect(self.screen, color, rect)
                row.append(rect)
            cells.append(row)

        if return_cells:
            return cells

    def neighbors(self, state: tuple, wall_included=False) -> list:
        row, col = state
        actions = {
            "UP": (row - 1, col),
            "DOWN": (row + 1, col),
            "LEFT": (row, col - 1),
            "RIGHT": (row, col + 1)
        }
        res = []
        for action, (r, c) in actions.items():
            if not wall_included:
                if 0 <= r < self.v_cells and 0 <= c < self.h_cells and \
                        (r, c) not in self.wall:
                    res.append([action, (r, c)])
            else:
                if 0 <= r < self.v_cells and 0 <= c < self.h_cells:
                    res.append([action, (r, c)])

        return res if len(res) != 0 else None

    def reset(self):
        self.wall = set()
        self.visited = set()
        self.path = list()
        self.start = None
        self.target = None

    def clear_visited(self):
        self.visited = set()
        self.path = list()

    def get_board_state(self) -> dict:
        state = {
            "start": self.start,
            "target": self.target,
            "path": self.path
        }
        return state


class Maze:
    """
    The Maze class is a maze generator and the main process of generating a maze using the random Prim algorithm.
    """
    def __init__(self, board: Board):
        self.board = board

    def initialize(self):
        self.board.wall = set((i, j) for i in range(self.board.v_cells) for j in range(self.board.h_cells))
        self.passages = {self.board.start}
        self.board.wall -= self.passages
        self.board.frontiers = self.get_frontiers(self.board.start)

    def get_frontiers(self, state: tuple) -> set:
        x, y = state
        frontiers = {(x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)}
        frontiers &= self.board.wall
        frontiers -= self.passages
        return frontiers

    def frontier_neighbor(self, frontier: tuple) -> tuple:
        x, y = frontier
        neighbors = {(x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)}
        neighbors &= self.passages
        return random.choice(tuple(neighbors))

    def connect_cell(self, cell_1: tuple, cell_2: tuple):
        x1, y1 = cell_1
        x2, y2 = cell_2

        x_conn = (x1 + x2) // 2 if x1 != x2 else x1
        y_conn = (y1 + y2) // 2 if y1 != y2 else y1

        if (x_conn, y_conn) in self.board.wall:
            self.passages.add((x_conn, y_conn))
            self.board.wall.remove((x_conn, y_conn))

    def generate(self):
        if not self.board.frontiers:
            raise ValueError("Use initialize function first")

        while self.board.frontiers:
            self.board.draw_board(return_cells=False)

            frontier = random.choice(tuple(self.board.frontiers))
            self.passages.add(frontier)

            neighbor = self.frontier_neighbor(frontier)
            self.connect_cell(frontier, neighbor)

            next_frontiers = self.get_frontiers(frontier)
            self.board.frontiers |= next_frontiers

            self.board.frontiers.remove(frontier)
            self.board.wall.remove(frontier)

            pygame.display.flip()
            time.sleep(0.02)
