import sys
from Constants import *
from Algorithms import *
from Maze import *


class Game:

    def __init__(self):
        self.__RUNNING = True
        self.__SEARCH = False
        self.__DRAW = False
        self.__ERASE = False
        self.__RESET = False
        self.__ALGO = None
        self.__PRESS = False
        self.__TIME = 0.1
        self.__board = Board(v_cells, h_cells, board_start[0], board_start[1], cell_size, screen, colors)

    def main_loop(self):
        while self.__RUNNING:
            # EXIT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Background filling
            screen.fill(colors["black"])

            if not self.__SEARCH:
                # Drawing a board and coordinates of cells,
                # to draw or erase walls in maze.
                cells = self.__board.draw_board()

                # Drawing buttons
                start_button()
                draw_button()
                erase_button()
                maze_button()
                reset_button()

                # Drawing an algorithms buttons
                dijkstra_button()
                astar_man_button()
                astar_evk_button()

                # If RESET pressed
                if self.__RESET:
                    time.sleep(self.__TIME)
                    reset_button.color_change(colors["crimson"])
                    reset_button()
                    self.__RESET = False

                    # Writing if RESET pressed to the file
                    result_file.write("RESET pressed\n")

                # Mouse-buttons pressed
                left, _, right = pygame.mouse.get_pressed()

                # If LEFT-button pressed
                if left == 1:
                    mouse = pygame.mouse.get_pos()

                    # Buttons colors when pressed,START-Button
                    if start_button.rect.collidepoint(mouse):
                        if not self.__SEARCH:
                            self.__SEARCH = True
                            self.__DRAW = False
                            self.__ERASE = False

                            draw_button.color_change(colors["white"])
                            erase_button.color_change(colors["white"])
                            start_button.color_change(colors["yellow"])

                            start_button()
                            draw_button()
                            erase_button()

                            time.sleep(self.__TIME)

                    # DRAW-Button
                    elif draw_button.rect.collidepoint(mouse):
                        if not self.__DRAW:
                            self.__DRAW = True
                            self.__ERASE = False
                            draw_button.color_change(colors["yellow"])
                            erase_button.color_change(colors["white"])
                        else:
                            self.__DRAW = False
                            draw_button.color_change(colors["white"])

                        time.sleep(self.__TIME)

                    # ERASE-Button
                    elif erase_button.rect.collidepoint(mouse):
                        if not self.__ERASE:
                            self.__ERASE = True
                            self.__DRAW = False
                            erase_button.color_change(colors["yellow"])
                            draw_button.color_change(colors["white"])
                        else:
                            self.__ERASE = False
                            erase_button.color_change(colors["white"])

                        time.sleep(self.__TIME)

                    # RESET-Button
                    elif reset_button.rect.collidepoint(mouse):
                        self.__DRAW = False
                        self.__ERASE = False
                        self.__RESET = True

                        draw_button.color_change(colors["white"])
                        erase_button.color_change(colors["white"])
                        reset_button.color_change(colors["yellow"])

                        reset_button()
                        self.__board.reset()

                        time.sleep(self.__TIME)

                    # MAZE-Button
                    elif maze_button.rect.collidepoint(mouse):
                        if self.__board.wall:
                            print("Please press RESET(button) to reset the Board")
                            time.sleep(self.__TIME)
                            continue

                        if not self.__board.start:
                            print("Please select START(target) to generate MAZE")
                            time.sleep(self.__TIME)
                            continue

                        elif self.__board.target:
                            print(
                                "Please do not set FINISH(target), you need "
                                "just to select start target and than you can generate maze")
                            time.sleep(self.__TIME)
                            continue

                        self.__DRAW = False
                        self.__ERASE = False
                        draw_button.color_change(colors["white"])
                        erase_button.color_change(colors["white"])
                        maze_button.color_change(colors["yellow"])

                        maze_button()

                        maze_creator = Maze(self.__board)
                        maze_creator.initialize()
                        maze_creator.generate()

                        maze_button.color_change(colors["white"])
                        maze_button()

                        time.sleep(self.__TIME)

                    # Choosing Algorithm, Dijkstra
                    if dijkstra_button.rect.collidepoint(mouse):
                        self.__ALGO = "Dijkstra"

                        dijkstra_button.color_change(colors["yellow"])
                        astar_man_button.color_change(colors["white"])
                        astar_evk_button.color_change(colors["white"])

                        time.sleep(self.__TIME)

                    # А* manhattan
                    elif astar_man_button.rect.collidepoint(mouse):
                        self.__ALGO = "AStarManhattan"

                        astar_man_button.color_change(colors["yellow"])
                        dijkstra_button.color_change(colors["white"])
                        astar_evk_button.color_change(colors["white"])

                        time.sleep(self.__TIME)

                    # А* euclidian
                    elif astar_evk_button.rect.collidepoint(mouse):
                        self.__ALGO = "AStarEuclidean"

                        astar_evk_button.color_change(colors["yellow"])
                        astar_man_button.color_change(colors["white"])
                        dijkstra_button.color_change(colors["white"])

                        time.sleep(self.__TIME)

                    # Drawing and Erasing Logic
                    else:
                        for i in range(v_cells):
                            for j in range(h_cells):
                                cell = cells[i][j]
                                if (i, j) != self.__board.start or (i, j) != self.__board.target:
                                    if self.__DRAW and cell.collidepoint(mouse):
                                        self.__board.wall.add((i, j))
                                    elif self.__ERASE and cell.collidepoint(mouse) and (i, j) in self.__board.wall:
                                        self.__board.wall.remove((i, j))

                # Right-Button pressed(Erasing targets)
                elif right == 1:
                    mouse = pygame.mouse.get_pos()

                    for i in range(v_cells):
                        for j in range(h_cells):
                            cell = cells[i][j]
                            if cell.collidepoint(mouse):
                                # if it's not wall and start has not been created, create start
                                if (i, j) not in self.__board.wall and self.__board.start is None:
                                    self.__board.start = (i, j)
                                # if it's not wall and start, and target has not been created, create target
                                elif (i, j) not in self.__board.wall and (
                                        i, j) != self.__board.start and self.__board.target is None:
                                    self.__board.target = (i, j)
                                # if it's start and target has not been created, chancel start
                                elif (i, j) == self.__board.start and self.__board.target is None:
                                    self.__board.start = None
                                # if it's target, chancel target
                                elif (i, j) == self.__board.target:
                                    self.__board.target = None

                    time.sleep(self.__TIME)

                pygame.display.flip()

            # Start Search
            else:
                # If START and FINISH is None
                if self.__board.start is None or self.__board.target is None:
                    print("Please choose position of START(target) and FINISH(target) to search")
                    self.__SEARCH = False
                    start_button.color_change(colors["green"])
                    continue

                # IF ALGO is None
                elif self.__ALGO is None:
                    print("Please choose algorithm")
                    self.__SEARCH = False
                    start_button.color_change(colors["green"])
                    continue

                if self.__board.visited or self.__board.path:
                    self.__board.clear_visited()

                # Using Algorithm that user choose
                if self.__ALGO == "Dijkstra":
                    algorithm = Dijkstra(self.__board)
                    algorithm.make_info()
                    algorithm.finding_path()

                elif self.__ALGO == "AStarManhattan":
                    algorithm = AStarManhattan(self.__board)
                    algorithm.make_info()
                    algorithm.finding_path()

                elif self.__ALGO == "AStarEuclidean":
                    algorithm = AStarEuclidean(self.__board)
                    algorithm.make_info()
                    algorithm.finding_path()

                # If PATH found
                if algorithm.find:
                    algorithm.output()

                    # Write the results to the file
                    result_file.write("\nPath Found!\n")
                    result_file.write("Algorithm used: " + self.__ALGO + "\n")

                    state = self.__board.get_board_state()
                    result_file.write("1)Start: " + str(state["start"]) + "\n")
                    result_file.write("2)Target: " + str(state["target"]) + "\n")
                    result_file.write("3)Path: " + str(state["path"]) + "\n")

                else:
                    print("Hmm, there is no solution..")

                    # Write the results to the file
                    result_file.write("\nPath not Found!\n")
                    result_file.write("Algorithm used: " + self.__ALGO + "\n")

                # RESTART
                self.__SEARCH = False
                start_button.color_change(colors["green"])

        # Close File
        result_file.close()

    # FPS
    CLOCK.tick(FPS)
