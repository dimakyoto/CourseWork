import time
import heapq
from Environment import *
from collections import defaultdict
from abc import ABCMeta, abstractmethod

INF = float('inf')
FREEZETIME = 0.01
DISTANCE = 1

class Search(metaclass=ABCMeta):

    #Абстрактний базовий класс
    @abstractmethod

    def finding_path(self):
        # Шукає найкоротший шлях
        pass

    def make_info(self):
        # інформація для розв'зку задачі певним алгоритмом
        pass

    def output(self):
        # Отримуються комірки для малювання дошки
        cells = self.board.draw_board()

        # Знаходиться найкоротший шлях, починаючи з цільового вузла і розвернутає його
        node = self.target_node
        while node.parent is not None:
            self.board.path.append(node.state)
            node = node.parent
        self.board.path.reverse()

        # Малює шлях
        color = self.board.colors["gold"]
        for i, j in self.board.path:
            time.sleep(1.5 * FREEZETIME)
            rect = cells[i][j]
            pygame.draw.rect(self.board.screen, color, rect)
            pygame.display.flip()


class Dijkstra(Search):

    def __init__(self, board: Board):
        self.board = board
        self.find = False

    def  make_info(self):
        # 1. Список сусідніх клітинок 2. Створює словники node_dict  3. і distance для зберігання вузлів та відстаней між вузлами та початковим вузлом.

        self.node_dict = {}
        self.distance = {}

        # створення вузлів
        for i in range(self.board.v_cells):
            for j in range(self.board.h_cells):
                # якщо (i, j) є стіною, не створювати вузол
                if (i, j) in self.board.wall:
                    continue

                pos = (i, j)
                node = Node(pos, None, None)
                if pos == self.board.start:
                    self.start_node = node
                elif pos == self.board.target:
                    self.target_node = node

                self.node_dict[pos] = node
                self.distance[node] = INF

        self.distance[self.start_node] = 0

        # додавання сусідніх вузлів до списку сусідів з дією та відстанню
        self.adj_list = defaultdict(dict)
        for _, node in self.node_dict.items():
            # отримати можливі позиції сусідніх вузлів
            neighbors = self.board.neighbors(node.state)
            for action, (row, col) in neighbors:
                # отримати сусідній вузол зі словника вузлів
                neighbor_node = self.node_dict[(row, col)]
                # оновити список сусідів
                self.adj_list[node][neighbor_node] = [action, DISTANCE]

    def update_distance_and_enqueue(self, node: Node, neighbor: Node):
        # Оновлює словник distance для кожного вузла та додає вузол у чергу за допомогою відстані.

        if self.distance[neighbor] > self.distance[node] + self.adj_list[node][neighbor][1]:
            # оновити відстань
            self.distance[neighbor] = self.distance[node] + self.adj_list[node][neighbor][1]

            # оновити батька та дію
            neighbor.parent = node
            neighbor.action = self.adj_list[node][neighbor][0]

            # додати сусіда до черги
            self.entry_count += 1
            heapq.heappush(self.heap, (self.distance[neighbor], self.entry_count, neighbor))

    def finding_path(self):
        # Під час додавання вузла до черги та якщо існують рівні значення відстаней,
        # черга буде розташовувати ці вузли у порядку часу вступу.

        self.heap = []
        self.entry_count = 1
        heapq.heappush(self.heap, (self.distance[self.start_node], self.entry_count, self.start_node))

        while self.heap and self.find == False:
            time.sleep(FREEZETIME)
            # Вилучення мінімального елемента
            (_, _, node) = heapq.heappop(self.heap)

            # Якщо знайдено цільовий вузол, встановити self.find == True
            if node.state == self.target_node.state:
                self.find = True

            # Позначити вузол як відвіданий
            self.board.visited.add(node)
            self.board.draw_board(return_cells=False)

            # Якщо вузол не має вихідних ребер, продовжувати цикл while
            if not self.adj_list[node]:
                continue

            # Якщо є вихідні ребра, ітерувати через всі ребра
            for neighbor in self.adj_list[node]:
                if neighbor not in self.board.visited:
                    self.update_distance_and_enqueue(node, neighbor)

            pygame.display.flip()


class AStar_man(Search):

    def __init__(self, board: Board):
        self.board = board
        self.find = False

    def  make_info(self):
        # 1. Список сусідніх клітинок 2. Створює словники node_dict(ключ - координати вершини; значення - сама вершина) 3. словник g_scores 4. словник h_scores

        self.node_dict = {}
        self.g_scores = {}
        self.h_scores = {}

        for i in range(self.board.v_cells):
            for j in range(self.board.h_cells):
                if (i, j) in self.board.wall:
                    continue

                pos = (i, j)
                node = Node(pos, None, None)
                if pos == self.board.start:
                    self.start_node = node
                elif pos == self.board.target:
                    self.target_node = node

                self.node_dict[pos] = node
                self.g_scores[node] = INF
                self.h_scores[node] = 0

        self.g_scores[self.start_node] = 0

        self.adj_list = defaultdict(dict)
        for _, node in self.node_dict.items():
            neighbors = self.board.neighbors(node.state)
            for action, (row, col) in neighbors:
                neighbor_node = self.node_dict[(row, col)]
                self.adj_list[node][neighbor_node] = [action, DISTANCE]

    def update_distance_and_enqueue(self, node: Node, neighbor: Node):

        # оновлюється значення g_scores для кожного вузла та додається вузол до черги згідно зі значеннями g_scores та h_scores.

        """
        node: selected visited node --> Node
        neighbor: neighboring nodes haven't been visited --> Node
        """

        # Якщо значення g_scores для сусіднього вузла більше, ніж сума значень g_scores поточного вузла та відстані до сусіднього вузла:
        if self.g_scores[neighbor] > self.g_scores[node] + self.adj_list[node][neighbor][1]:
            # оновити відстань
            self.g_scores[neighbor] = self.g_scores[node] + self.adj_list[node][neighbor][1]

            # оновити батька та виконану дію
            neighbor.parent = node
            neighbor.action = self.adj_list[node][neighbor][0]

            # додати сусіда до черги
            self.entry_count += 1
            self.h_scores[neighbor] = AStar_man.manhattan(neighbor, self.target_node)
            heapq.heappush(self.heap, (self.g_scores[neighbor] + self.h_scores[neighbor], self.entry_count, neighbor))

    @staticmethod
    def manhattan(node_1: Node, node_2: Node) -> int:
        """
        У статичному методі manhattan обчислюється відстань між двома вузлами за допомогою мангаттанської метрики.

        node_1: first node to be computed --> Node
        node_2: second node to be computed --> Node
        """

        start_x, start_y = node_1.state
        target_x, target_y = node_2.state
        return abs(start_x - target_x) + abs(start_y - target_y)

    def finding_path(self):
        # Під час додавання вузла до черги та якщо існують рівні значення відстаней,
        # черга буде розташовувати ці вузли у порядку часу вступу.

        self.heap = []
        self.entry_count = 1
        h_score_s2t = AStar_man.manhattan(self.start_node, self.target_node)  # h_score від початку до цільового вузла
        heapq.heappush(self.heap, (h_score_s2t, self.entry_count, self.start_node))

        while self.heap and not self.find:
            time.sleep(FREEZETIME)
            # Вилучення мінімального елемента
            _, _, node = heapq.heappop(self.heap)

            # Якщо знайдено цільовий вузол, встановити self.find == True
            if node.state == self.target_node.state:
                self.find = True

            # Позначити вузол як відвіданий
            self.board.visited.add(node)
            self.board.draw_board(return_cells=False)

            # Якщо вузол не має вихідних ребер, продовжувати цикл while
            if not self.adj_list[node]:
                continue

            # Якщо є вихідні ребра, ітерувати через всі ребра
            for neighbor in self.adj_list[node]:
                if neighbor not in self.board.visited:
                    self.update_distance_and_enqueue(node, neighbor)

            pygame.display.flip()


class AStar_evk(Search):

    def __init__(self, board: Board):
        self.board = board
        self.find = False

    def  make_info(self):

         # 1. Список сусідніх клітинок 2. Створює словники node_dict(ключ - координати вершини; значення - сама вершина) 3. словник g_scores 4. словник h_scores

        self.node_dict = {}
        self.g_scores = {}
        self.h_scores = {}

        for i in range(self.board.v_cells):
            for j in range(self.board.h_cells):
                if (i, j) in self.board.wall:
                    continue

                pos = (i, j)
                node = Node(pos, None, None)
                if pos == self.board.start:
                    self.start_node = node
                elif pos == self.board.target:
                    self.target_node = node

                self.node_dict[pos] = node
                self.g_scores[node] = INF
                self.h_scores[node] = 0

        self.g_scores[self.start_node] = 0

        self.adj_list = defaultdict(dict)
        for _, node in self.node_dict.items():
            neighbors = self.board.neighbors(node.state)
            for action, (row, col) in neighbors:
                neighbor_node = self.node_dict[(row, col)]
                self.adj_list[node][neighbor_node] = [action, DISTANCE]

    def update_distance_and_enqueue(self, node: Node, neighbor: Node):

        # оновлюється значення g_scores для кожного вузла та додається вузол до черги згідно зі значеннями g_scores та h_scores.

        """
        node: selected visited node --> Node
        neighbor: neighboring nodes haven't been visited --> Node
        """
        if self.g_scores[neighbor] > self.g_scores[node] + self.adj_list[node][neighbor][1]:
            # оновити відстань
            self.g_scores[neighbor] = self.g_scores[node] + self.adj_list[node][neighbor][1]

            # оновити батька та дію
            neighbor.parent = node
            neighbor.action = self.adj_list[node][neighbor][0]

            # додати сусіда до черги
            self.entry_count += 1
            self.h_scores[neighbor] = AStar_evk.euclidean(neighbor, self.target_node)
            heapq.heappush(self.heap, (self.g_scores[neighbor] + self.h_scores[neighbor], self.entry_count, neighbor))

    @staticmethod
    def euclidean(node_1: Node, node_2: Node) -> float:

        """
        У статичному методі euclidean обчислюється відстань між двома вузлами за допомогою евклідової метрики.
        node_1: first node to be computed --> Node
        node_2: second node to be computed --> Node
        """

        start_x, start_y = node_1.state
        target_x, target_y = node_2.state
        return ((start_x - target_x) ** 2 + (start_y - target_y) ** 2) ** 0.5

    def finding_path(self):

        # При додаванні вузла у купу (heap) з однаковими значеннями відстані,
        # купа буде впорядковувати ці вузли за часом їх входу.
        self.heap = []
        self.entry_count = 1
        h_score_s2t = AStar_evk.euclidean(self.start_node, self.target_node)
        heapq.heappush(self.heap, (h_score_s2t, self.entry_count, self.start_node))

        while self.heap and not self.find:
            time.sleep(FREEZETIME)
            # Вилучення найменшого
            _, _, node = heapq.heappop(self.heap)

            # Якщо знайдено цільовий вузол, встановити self.find == True
            if node.state == self.target_node.state:
                self.find = True

            # Позначити вузол як відвіданий
            self.board.visited.add(node)
            self.board.draw_board(return_cells=False)

            # Якщо немає вихідних ребер, продовжити цикл while
            if not self.adj_list[node]:
                continue

            # Якщо є вихідні ребра, перебір усіх ребер
            for neighbor in self.adj_list[node]:
                if neighbor not in self.board.visited:
                    self.update_distance_and_enqueue(node, neighbor)

            pygame.display.flip()



