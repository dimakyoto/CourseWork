import time
import heapq
from Environment import *
from collections import defaultdict
from abc import ABCMeta, abstractmethod


class Search(metaclass=ABCMeta):

    def __init__(self):
        self._INF = float('inf')
        self._TIME = 0.01
        self._DISTANCE = 1
        self.visited_cells = 0
        self.comparisons = 0
        self.swaps = 0
        self.start_time = 0
        self.execution_time = 0
        self.end_time = 0


    @abstractmethod
    def finding_path(self):
        # Method finding the shortest path
        pass

    @abstractmethod
    def make_info(self):
        # Method making info for algorithms
        pass

    def output(self):
        # Method drawing path
        cells = self.board.draw_board()

        # The shortest path, then reverse
        node = self.target_node
        while node.parent is not None:
            self.board.path.append(node.state)
            node = node.parent
        self.board.path.reverse()

        # Drawing path
        color = self.board.colors["gold"]

        for i, j in self.board.path:
            time.sleep(1.5 * self._TIME)
            rect = cells[i][j]
            pygame.draw.rect(self.board.screen, color, rect)
            pygame.display.flip()

    def get_info(self):
        execution_time = round(self.execution_time, 2)
        return {
            'iterations': self.swaps,
            'comparisons': self.comparisons,
            'visited_cells': self.visited_cells,
            'execution_time': execution_time
        }


class Dijkstra(Search):

    def __init__(self, board: Board):
        super().__init__()
        self.board = board
        self.find = False

    def make_info(self):
        """
        1) List of neighboring cells.
        2) Creates node dictionaries.
        3) Creates distance dictionaries for storing nodes and distances between nodes and the starting node.
        """
        self.node_dict = {}
        self.distance = {}
        self.start_time = time.time()

        # Create nodes
        for i in range(self.board.v_cells):
            for j in range(self.board.h_cells):
                # If (i, j) is a wall, do not create a node
                if (i, j) in self.board.wall:
                    continue

                pos = (i, j)
                node = Node(pos, None, None)
                if pos == self.board.start:
                    self.start_node = node
                elif pos == self.board.target:
                    self.target_node = node

                self.node_dict[pos] = node
                self.distance[node] = self._INF
                self.visited_cells += 1

        self.distance[self.start_node] = 0

        # Add neighboring nodes to the adjacency list with action and distance
        self.adj_list = defaultdict(dict)
        for _, node in self.node_dict.items():
            # Get possible positions of neighboring nodes
            neighbors = self.board.neighbors(node.state)
            for action, (row, col) in neighbors:
                # Get the neighboring node from the node dictionary
                neighbor_node = self.node_dict[(row, col)]
                # Update the adjacency list
                self.adj_list[node][neighbor_node] = [action, self._DISTANCE]

    def update_distance_and_enqueue(self, node: Node, neighbor: Node):
        """
        Updates the distance dictionary for each node and enqueues the node based on distance.
        """
        if self.distance[neighbor] > self.distance[node] + self.adj_list[node][neighbor][1]:
            self.comparisons += 1
            # Update the distance
            self.distance[neighbor] = self.distance[node] + self.adj_list[node][neighbor][1]

            # Update the parent and action
            neighbor.parent = node
            neighbor.action = self.adj_list[node][neighbor][0]

            # Add the neighbor to the queue
            self.swaps += 1
            self.entry_count += 1
            heapq.heappush(self.heap, (self.distance[neighbor], self.entry_count, neighbor))

    def finding_path(self):
        """
        During node enqueueing, if there are equal distance values, the queue will prioritize nodes based on entry time.
        """

        self.heap = []
        self.entry_count = 1
        heapq.heappush(self.heap, (self.distance[self.start_node], self.entry_count, self.start_node))

        while self.heap and not self.find:
            time.sleep(self._TIME)
            # Extract the minimum element
            (_, _, node) = heapq.heappop(self.heap)

            # If the target node is found, set self.find to True
            if node.state == self.target_node.state:
                self.find = True

            # Mark the node as visited
            self.board.visited.add(node)
            self.board.draw_board(return_cells=False)

            # If the node has no outgoing edges, continue the while loop
            if not self.adj_list[node]:
                continue

            # If there are outgoing edges, iterate through all the edges
            for neighbor in self.adj_list[node]:
                if neighbor not in self.board.visited:
                    self.update_distance_and_enqueue(node, neighbor)

            self.end_time = time.time()
            self.execution_time = self.end_time - self.start_time
            pygame.display.flip()


class AStarManhattan(Search):
    def __init__(self, board: Board):
        super().__init__()
        self.board = board
        self.find = False

    def make_info(self):
        """
        Creates necessary data structures for the A* Manhattan algorithm:
        1. node_dict: dictionary mapping node coordinates to node objects.
        2. g_scores: dictionary to store the g-scores (path costs) for each node.
        3. h_scores: dictionary to store the h-scores (heuristic estimates) for each node.
        """

        self.node_dict = {}
        self.g_scores = {}
        self.h_scores = {}
        self.start_time = time.time()

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
                self.g_scores[node] = self._INF
                self.visited_cells += 1
                self.h_scores[node] = 0

        self.g_scores[self.start_node] = 0

        self.adj_list = defaultdict(dict)
        for _, node in self.node_dict.items():
            neighbors = self.board.neighbors(node.state)
            for action, (row, col) in neighbors:
                neighbor_node = self.node_dict[(row, col)]
                self.adj_list[node][neighbor_node] = [action, self._DISTANCE]

    def update_distance_and_enqueue(self, node: Node, neighbor: Node):
        """
        Updates the g-scores for each node and enqueues the neighbor node based on the g-scores and h-scores.
        """
        if self.g_scores[neighbor] > self.g_scores[node] + self.adj_list[node][neighbor][1]:
            self.comparisons += 1
            self.g_scores[neighbor] = self.g_scores[node] + self.adj_list[node][neighbor][1]
            neighbor.parent = node
            neighbor.action = self.adj_list[node][neighbor][0]
            self.swaps += 1
            self.entry_count += 1
            self.h_scores[neighbor] = AStarManhattan.manhattan(neighbor, self.target_node)
            heapq.heappush(self.heap, (self.g_scores[neighbor] + self.h_scores[neighbor], self.entry_count, neighbor))

    @staticmethod
    def manhattan(node_1: Node, node_2: Node) -> int:
        """
        Computes the Manhattan distance between two nodes.
        """
        start_x, start_y = node_1.state
        target_x, target_y = node_2.state
        return abs(start_x - target_x) + abs(start_y - target_y)

    def finding_path(self):
        """
        During node enqueueing, if there are equal distance values, the queue will prioritize nodes based on entry time.
        """
        self.heap = []
        self.entry_count = 1

        h_score_s2t = AStarManhattan.manhattan(self.start_node, self.target_node)
        heapq.heappush(self.heap, (h_score_s2t, self.entry_count, self.start_node))

        while self.heap and not self.find:
            time.sleep(self._TIME)
            _, _, node = heapq.heappop(self.heap)

            if node.state == self.target_node.state:
                self.find = True

            self.board.visited.add(node)
            self.board.draw_board(return_cells=False)

            if not self.adj_list[node]:
                continue

            for neighbor in self.adj_list[node]:
                if neighbor not in self.board.visited:
                    self.update_distance_and_enqueue(node, neighbor)

            self.end_time = time.time()
            self.execution_time = self.end_time - self.start_time
            pygame.display.flip()


class AStarEuclidean(Search):
    def __init__(self, board: Board):
        super().__init__()  # Call the parent class constructor
        self.board = board
        self.find = False

    def make_info(self):
        """
        Creates necessary data structures for the A* Euclidean algorithm:
        1. node_dict: dictionary mapping node coordinates to node objects.
        2. g_scores: dictionary to store the g-scores (path costs) for each node.
        3. h_scores: dictionary to store the h-scores (heuristic estimates) for each node.
        """

        self.node_dict = {}
        self.g_scores = {}
        self.h_scores = {}
        self.start_time = time.time()

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
                self.g_scores[node] = self._INF
                self.visited_cells += 1
                self.h_scores[node] = 0

        self.g_scores[self.start_node] = 0

        self.adj_list = defaultdict(dict)
        for _, node in self.node_dict.items():
            neighbors = self.board.neighbors(node.state)
            for action, (row, col) in neighbors:
                neighbor_node = self.node_dict[(row, col)]
                self.adj_list[node][neighbor_node] = [action, self._DISTANCE]

    def update_distance_and_enqueue(self, node: Node, neighbor: Node):
        """
        Updates the g-scores for each node and enqueues the neighbor node based on the g-scores and h-scores.
        """
        if self.g_scores[neighbor] > self.g_scores[node] + self.adj_list[node][neighbor][1]:
            self.comparisons += 1
            self.g_scores[neighbor] = self.g_scores[node] + self.adj_list[node][neighbor][1]
            neighbor.parent = node
            neighbor.action = self.adj_list[node][neighbor][0]
            self.swaps += 1
            self.entry_count += 1
            self.h_scores[neighbor] = AStarEuclidean.euclidean(neighbor, self.target_node)
            heapq.heappush(self.heap, (self.g_scores[neighbor] + self.h_scores[neighbor], self.entry_count, neighbor))

    @staticmethod
    def euclidean(node_1: Node, node_2: Node) -> float:
        """
        Computes the Euclidean distance between two nodes.
        """
        start_x, start_y = node_1.state
        target_x, target_y = node_2.state
        return ((start_x - target_x) ** 2 + (start_y - target_y) ** 2) ** 0.5

    def finding_path(self):
        """
        Finds the path using the A* Euclidean algorithm.
        During node enqueueing, if there are equal distance values, the queue will prioritize nodes based on entry time.
        """
        self.heap = []
        self.entry_count = 1

        h_score_s2t = AStarEuclidean.euclidean(self.start_node, self.target_node)
        heapq.heappush(self.heap, (h_score_s2t, self.entry_count, self.start_node))

        while self.heap and not self.find:
            time.sleep(self._TIME)
            _, _, node = heapq.heappop(self.heap)

            if node.state == self.target_node.state:
                self.find = True

            self.board.visited.add(node)
            self.board.draw_board(return_cells=False)

            if not self.adj_list[node]:
                continue

            for neighbor in self.adj_list[node]:
                if neighbor not in self.board.visited:
                    self.update_distance_and_enqueue(node, neighbor)

            self.end_time = time.time()
            self.execution_time = self.end_time - self.start_time
            pygame.display.flip()
