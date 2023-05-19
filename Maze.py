import time
import random
from Environment import *

class Maze:
    def __init__(self, board: Board):
        self.board = board

    def initialize(self):
        """
        Initializes the maze generation process:
        1. Sets all cells as walls, except for the start and target cells.
        2. Sets the start and target cells as passages to record the maze path.
        3. Adds frontiers to the board frontiers for the start and target cells.
        """
        self.board.wall = {(i, j) for i in range(self.board.v_cells) for j in range(self.board.h_cells)}
        self.passages = {self.board.start}
        self.board.wall = self.board.wall.difference(self.passages)
        self.board.frontiers = self.get_frontiers(self.board.start)

    def get_frontiers(self, state: tuple) -> set:
        """
        Returns the set of frontiers for a given cell.
        Frontiers are cells that are walls and are at a distance of 2 (in a straight direction) from the given cell.

        state: position of node --> tuple
        """
        x, y = state
        frontiers = {(x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)}
        temp_frontiers = frontiers.copy()
        for row, col in temp_frontiers:
            if (row < 0 or row >= self.board.v_cells) or (col < 0 or col >= self.board.h_cells) or \
                    (row, col) in self.passages or (row, col) not in self.board.wall:
                frontiers.remove((row, col))
        return frontiers

    def frontier_neighbor(self, frontier: tuple) -> tuple:
        """
        Randomly selects a cell that is at a distance of 2 from cells in the passage from the selected frontier.

        frontier: position of frontier --> tuple
        """
        t = int(time.time())
        random.seed(t)

        x, y = frontier
        neighbors = {(x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)}

        temp_neighbors = neighbors.copy()
        for cell in temp_neighbors:
            if cell not in self.passages:
                neighbors.remove(cell)

        neighbor = random.choice(list(neighbors))
        return neighbor

    def connect_cell(self, cell_1: tuple, cell_2: tuple):
        """
        Connects cells by changing the wall between the passage and the selected neighbor of the frontier.

        cell_1: first cell to be connected --> tuple
        cell_2: second cell to be connected --> tuple
        """
        x1, y1 = cell_1
        x2, y2 = cell_2

        x_diff = x1 - x2
        y_diff = y1 - y2

        if x_diff != 0 and y_diff == 0:
            x_conn = (x1 + x2) // 2
            y_conn = y1

        elif y_diff != 0 and x_diff == 0:
            y_conn = (y1 + y2) // 2
            x_conn = x1

        if (x_conn, y_conn) in self.board.wall:
            self.passages.add((x_conn, y_conn))
            self.board.wall.remove((x_conn, y_conn))

    def generate(self):
        """
        Main function for generating the maze using the random Prim's algorithm.
        """
        if not self.board.frontiers:
            raise ValueError("use initialize function first")

        while self.board.frontiers:
            t = int(time.time())
            random.seed(t)
            time.sleep(0.01)
            self.board.draw_board(return_cells=False)

            # Randomly choose a cell from the frontiers and add it to the passages set
            frontier = random.choice(list(self.board.frontiers))
            self.passages.add(frontier)

            # Randomly choose a neighbor of the frontier cell and connect them by removing the wall
            neighbor = self.frontier_neighbor(frontier)
            self.connect_cell(frontier, neighbor)

            # Get new frontiers based on the selected frontier cell and add them to the board's frontiers set
            next_frontiers = self.get_frontiers(frontier)
            self.board.frontiers = self.board.frontiers | next_frontiers

            # Remove the current frontier cell from the board's frontiers set and the board's wall set
            self.board.frontiers.remove(frontier)
            self.board.wall.remove(frontier)

            pygame.display.flip()
