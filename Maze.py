import time
import random
from Environment import *

FREEZETIME = 0.01

class Maze:

    # використовується для генерації лабіринту за допомогою алгоритму випадкового Пріма

    def __init__(self, board: Board):
        self.board = board

    def initialize(self):

        """
        Ініціалізує інформацію для розв'язувача лабіринту
        1.self.board.wall - встановлює всі комірки як стіни, за винятком початкової і цільової комірок.
        2.self.passages - встановлює початкову і цільову комірки як прохід для запису шляху лабіринту.
        3.self.board.frontiers - додає до board.frontiers межі (фронтири) для початкової і цільової комірок.
        """

        # Спочатку встановлюємо кожну комірку як стіну
        self.board.wall = {
            (i, j) for i in range(self.board.v_cells)
            for j in range(self.board.h_cells)
        }

        # Додаємо початкову і цільову комірки до межі
        self.passages = {self.board.start}

        # Видаляємо початкову і цільову комірки зі стіни
        self.board.wall = self.board.wall.difference(self.passages)

        # Ініціалізуємо межу
        self.board.frontiers = self.get_frontiers(self.board.start)

    def get_frontiers(self, state: tuple) -> set:
        """
        Повертає множину межі для заданої комірки.
        Межі - це комірки, що є стінами та знаходяться на відстані 2 (в прямому напрямку) від заданої комірки.

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
        Випадковим чином вибирає комірку, що знаходиться на відстані 2 від комірок у проході з обраної межі.

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
        З'єднує комірки, змінюючи стіну між проходом та вибраним сусідом межі.

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
       Основна функція для генерації лабіринту за допомогою алгоритму випадкового Пріма
        """
        if not self.board.frontiers:
            raise ValueError("use initialze function first")

        while self.board.frontiers:
            t = int(time.time())
            random.seed(t)
            time.sleep(FREEZETIME)
            self.board.draw_board(return_cells=False)

            # Випадковим чином обрати одну клітину з фронтальних клітин та додати її до множини проходів (passages)
            frontier = random.choice(list(self.board.frontiers))
            self.passages.add(frontier)

            # Випадковим чином обрати сусіда фронтальної клітини та з'єднати їх шляхом
            neighbor = self.frontier_neighbor(frontier)
            self.connect_cell(frontier, neighbor)

            # Отримати нові фронтальні клітини, які обчислюються на основі вибраної фронтальної клітини та додати їх до множини фронтальних клітин дошки
            next_frontiers = self.get_frontiers(frontier)
            self.board.frontiers = self.board.frontiers | next_frontiers

            # Видалити поточну фронтальну клітину з множини фронтальних клітин дошки та з множини стін дошки
            self.board.frontiers.remove(frontier)
            self.board.wall.remove(frontier)

            pygame.display.flip()