import sys
from Constants import *
from Algorithms import *
from Maze import *

class Game:

    def __init__(self):
        self.RUNNING = True
        self.SEARCH = False
        self.DRAW = False
        self.ERASE = False
        self.RESET = False
        self.ALGO = None
        self.PRESS = False
        self.FREEZETIME = 0.1
        self.board = Board(v_cells, h_cells, board_start[0], board_start[1], cell_size, screen, colors)

    def main_loop(self):
        #  Мейн-цикл
        while self.RUNNING:
            # Вихід з проги
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #  Бекграунд
            screen.fill(colors["black"])

            if not self.SEARCH:
                # Малюється дошка та отримуються координати клітинок на дошці,
                # які використовуються для малювання та видалення стін.
                #
                cells = self.board.draw_board()

                # Малювання кнопок
                start_button()
                draw_button()
                erase_button()
                maze_button()
                reset_button()

                # Малювання кнопок алгоритму
                dijkstra_button()
                astar_man_button()
                astar_evk_button()

                # Натискання RESET
                if self.RESET:
                    time.sleep(0.05)
                    reset_button.color_change(colors["crimson"])
                    reset_button()
                    self.RESET = False

                    # Write the results to the file
                    result_file.write("RESET pressed\n")

                # Натискання на мишу
                left, _, right = pygame.mouse.get_pressed()

                # Якщо ліва кнопка миші натиснута
                if left == 1:
                    mouse = pygame.mouse.get_pos()

                    # Кнопки модифікацій лабіринту

                    # Кнопка старту
                    if start_button.rect.collidepoint(mouse):
                        if not self.SEARCH:
                            self.SEARCH = True
                            self.DRAW = False
                            self.ERASE = False

                            draw_button.color_change(colors["white"])
                            erase_button.color_change(colors["white"])
                            start_button.color_change(colors["yellow"])

                            start_button()
                            draw_button()
                            erase_button()

                            time.sleep(self.FREEZETIME)

                    # Кнопка рисування стін
                    elif draw_button.rect.collidepoint(mouse):
                        if not self.DRAW:
                            self.DRAW = True
                            self.ERASE = False
                            draw_button.color_change(colors["yellow"])
                            erase_button.color_change(colors["white"])
                        else:
                            self.DRAW = False
                            draw_button.color_change(colors["white"])

                        time.sleep(self.FREEZETIME)

                        # Кнопка видалення стін
                    elif erase_button.rect.collidepoint(mouse):
                        if not self.ERASE:
                            self.ERASE = True
                            self.DRAW = False
                            erase_button.color_change(colors["yellow"])
                            draw_button.color_change(colors["white"])
                        else:
                            self.ERASE = False
                            erase_button.color_change(colors["white"])

                        time.sleep(self.FREEZETIME)

                    # Кнопка RESET
                    elif reset_button.rect.collidepoint(mouse):
                        self.DRAW = False
                        self.ERASE = False
                        self.RESET = True

                        draw_button.color_change(colors["white"])
                        erase_button.color_change(colors["white"])
                        reset_button.color_change(colors["yellow"])

                        reset_button()
                        self.board.reset()

                        time.sleep(self.FREEZETIME)

                        # Кнопка генерації лабіринту
                    elif maze_button.rect.collidepoint(mouse):
                        if self.board.wall:
                            print("Please press RESET(button) to reset the Board")
                            time.sleep(self.FREEZETIME)
                            continue

                        if not self.board.start:
                            print("Please select START(target) to generate MAZE")
                            time.sleep(self.FREEZETIME)
                            continue

                        elif self.board.target:
                            print(
                                "Please do not set FINISH(target), you need "
                                "just to select start target and than you can generate maze")
                            time.sleep(FREEZETIME)
                            continue

                        self.DRAW = False
                        self.ERASE = False
                        draw_button.color_change(colors["white"])
                        erase_button.color_change(colors["white"])
                        maze_button.color_change(colors["yellow"])

                        maze_button()

                        maze_creator = Maze(self.board)
                        maze_creator.initialize()
                        maze_creator.generate()

                        maze_button.color_change(colors["white"])
                        maze_button()

                        time.sleep(self.FREEZETIME)

                    # Кнопки вибору алгоритмів

                    # Дейкстра
                    if dijkstra_button.rect.collidepoint(mouse):
                        self.ALGO = "Dijkstra"

                        dijkstra_button.color_change(colors["yellow"])
                        astar_man_button.color_change(colors["white"])
                        astar_evk_button.color_change(colors["white"])

                        time.sleep(self.FREEZETIME)


                    # А* манхетенська
                    elif astar_man_button.rect.collidepoint(mouse):
                        self.ALGO = "AStar_man"

                        astar_man_button.color_change(colors["yellow"])
                        dijkstra_button.color_change(colors["white"])
                        astar_evk_button.color_change(colors["white"])

                        time.sleep(self.FREEZETIME)

                        # А* евклідова
                    elif astar_evk_button.rect.collidepoint(mouse):
                        self.ALGO = "AStar_evk"

                        astar_evk_button.color_change(colors["yellow"])
                        astar_man_button.color_change(colors["white"])
                        dijkstra_button.color_change(colors["white"])

                        time.sleep(self.FREEZETIME)

                    # Малювання або стирання стіни
                    else:
                        for i in range(v_cells):
                            for j in range(h_cells):
                                cell = cells[i][j]
                                if (i, j) != self.board.start or (i, j) != self.board.target:
                                    if self.DRAW and cell.collidepoint(mouse):
                                        self.board.wall.add((i, j))
                                    elif self.ERASE and cell.collidepoint(mouse) and (i, j) in self.board.wall:
                                        self.board.wall.remove((i, j))

                # Натискання на праву кнопку, стирання старту або фінішу
                elif right == 1:
                    mouse = pygame.mouse.get_pos()

                    for i in range(v_cells):
                        for j in range(h_cells):
                            cell = cells[i][j]
                            if cell.collidepoint(mouse):
                                # if it's not wall and start has not been created, create start
                                if (i, j) not in self.board.wall and self.board.start is None:
                                    self.board.start = (i, j)
                                # if it's not wall and start, and target has not been created, create target
                                elif (i, j) not in self.board.wall and (i, j) != self.board.start and self.board.target is None:
                                    self.board.target = (i, j)
                                # if it's start and target has not been created, chancel start
                                elif (i, j) == self.board.start and self.board.target is None:
                                    self.board.start = None
                                # if it's target, chancel target
                                elif (i, j) == self.board.target:
                                    self.board.target = None

                    time.sleep(self.FREEZETIME)

                pygame.display.flip()


            # Початок пошуку
            else:
                # Якщо нема старту і кінця кіна не буде аххахаххаа
                if self.board.start is None or self.board.target is None:
                    print("Please choose position of START(target) and FINISH(target) to search")
                    self.SEARCH = False
                    start_button.color_change(colors["green"])
                    continue

                    # Не обрав алгоритм
                elif self.ALGO is None:
                    print("Please choose algorithm")
                    self.SEARCH = False
                    start_button.color_change(colors["green"])
                    continue

                if self.board.visited or self.board.path:
                    self.board.clear_visited()

                # Застосування обраного алгоритму
                if self.ALGO == "Dijkstra":
                    algorithm = Dijkstra(self.board)
                    algorithm.make_info()
                    algorithm.finding_path()


                elif self.ALGO == "AStar_man":
                    algorithm = AStar_man(self.board)
                    algorithm.make_info()
                    algorithm.finding_path()


                elif self.ALGO == "AStar_evk":
                    algorithm = AStar_evk(self.board)
                    algorithm.make_info()
                    algorithm.finding_path()

                # Якщо дорога знайдена
                if algorithm.find:
                    algorithm.output()

                    # Write the results to the file
                    result_file.write("\nPath Found!\n")
                    result_file.write("Algorithm used: " + self.ALGO + "\n")

                    state = self.board.get_board_state()
                    result_file.write("1)Start: " + str(state["start"]) + "\n")
                    result_file.write("2)Target: " + str(state["target"]) + "\n")
                    result_file.write("3)Path: " + str(state["path"]) + "\n")

                else:
                    print("Hmm, there is no solution..")

                    result_file.write("\nPath not Found!\n")
                    result_file.write("Algorithm used: " + self.ALGO + "\n")

                # Рестарт гри
                self.SEARCH = False
                start_button.color_change(colors["green"])

        result_file.close()
        CLOCK.tick(FPS)