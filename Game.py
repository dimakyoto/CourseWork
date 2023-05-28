import sys
from pygame.locals import *
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

        self.__v_cells = 50
        self.__h_cells = 50
        self.__cell_size = int(min(board_height / self.__v_cells, board_width / self.__h_cells))

        self.__board = Board(self.__v_cells, self.__h_cells, board_start[0], board_start[1], self.__cell_size, screen)

    def reset_algorithms_colors(self):
        astar_man_button.color_change(colors["white"])
        dijkstra_button.color_change(colors["white"])
        astar_evk_button.color_change(colors["white"])

    def reset_textfield(self):
        Comparisons.set_text("")
        Comparisons.draw(screen)
        Iterations.set_text("")
        Iterations.draw(screen)
        Visited_cells.set_text("")
        Visited_cells.draw(screen)
        Execution_time.set_text("")
        Execution_time.draw(screen)

    def enter_maze_size(self):
        color_active = pygame.Color(colors["blue"])
        color_inactive = pygame.Color(colors["deepskyblue"])

        color = color_inactive
        ACTIVE = False
        text = ""

        Instruction_text = Instruction_font.render("Enter size of the maze (e.g., 30): ", True, colors["black"])
        Instruction_text_rect = Instruction_text.get_rect(center=(WIDTH // 2, 275))

        Warning_text = ButtonFont.render("Warning: The input number must be between 10 and 50!", True,
                                         colors["crimson"])
        Warning_text_rect = Warning_text.get_rect(bottomleft=(10, HEIGHT - 10))

        cursor_color = pygame.Color("black")
        cursor_visible = True
        cursor_timer = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if input_line.collidepoint(event.pos):
                        ACTIVE = not ACTIVE
                    else:
                        ACTIVE = False
                    color = color_active if ACTIVE else color_inactive
                    if back_button.rect.collidepoint(event.pos):
                        return
                if event.type == KEYDOWN:
                    if ACTIVE:
                        if event.key == K_RETURN:
                            if not text.isdigit():
                                print("Please enter a valid size (numeric value, e.g., 30)")
                            else:
                                size = int(text)
                                if size < 10 or size > 50:
                                    print("Size must be between 10 and 50")
                                else:
                                    return size
                        elif event.key == K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
                            if len(text) > MAX_LENGTH:
                                text = text[:MAX_LENGTH]

            screen.fill(colors["gainsboro"])

            txt_surface = ButtonFont.render(text, True, colors["black"])
            width = max(200, txt_surface.get_width() + 10, MAX_LENGTH * ButtonFont.size(" ")[0])
            input_line.w = width

            screen.blit(Instruction_text, Instruction_text_rect)
            screen.blit(txt_surface, (input_line.x + 5, input_line.y + 5))
            pygame.draw.rect(screen, color, input_line, 2)
            screen.blit(Warning_text, Warning_text_rect)

            if ACTIVE:
                cursor_timer += CLOCK.get_time()
                if cursor_timer >= 500:
                    cursor_visible = not cursor_visible
                    cursor_timer = 0

            if cursor_visible and ACTIVE:
                cursor_pos = (input_line.x + txt_surface.get_width() + 10, input_line.y + 10)
                pygame.draw.line(screen, cursor_color, cursor_pos,
                                 (cursor_pos[0], cursor_pos[1] + input_line.height - 20), 2)

            back_button()
            pygame.display.flip()
            CLOCK.tick(FPS)

    def main_loop(self):
        while self.__RUNNING:
            # EXIT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            screen.fill(colors["black"])

            if not self.__SEARCH:

                cells = self.__board.draw_board()

                # Drawing control buttons
                start_button()
                maze_button()
                maze_size_button()
                draw_button()
                erase_button()
                reset_button()

                # Drawing an algorithms buttons
                Comparisons.draw(screen)
                Iterations.draw(screen)
                Visited_cells.draw(screen)
                Execution_time.draw(screen)
                dijkstra_button()
                astar_man_button()
                astar_evk_button()

                # If RESET pressed
                if self.__RESET:
                    time.sleep(self.__TIME)
                    reset_button.color_change(colors["crimson"])
                    reset_button()
                    self.__RESET = False
                    self.__ALGO = None

                    self.reset_textfield()

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

                            start_button.color_change(colors["yellow"])
                            draw_button.color_change(colors["white"])
                            erase_button.color_change(colors["white"])

                            start_button()

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

                        maze_button.color_change(colors["yellow"])
                        draw_button.color_change(colors["white"])
                        erase_button.color_change(colors["white"])

                        maze_button()

                        maze_creator = Maze(self.__board)
                        maze_creator.initialize()
                        maze_creator.generate()

                        maze_button.color_change(colors["white"])
                        maze_button()

                        time.sleep(self.__TIME)

                    # SIZE-Button
                    elif maze_size_button.rect.collidepoint(mouse):
                        if self.__board.wall:
                            print("Please press RESET(button) to reset the Board")
                            time.sleep(self.__TIME)
                            continue

                        self.__DRAW = False
                        self.__ERASE = False

                        maze_button.color_change(colors["white"])
                        maze_size_button.color_change(colors["yellow"])
                        draw_button.color_change(colors["white"])
                        erase_button.color_change(colors["white"])

                        new_size = self.enter_maze_size()

                        if new_size is None:
                            maze_size_button.color_change(colors["white"])
                            continue

                        maze_size_button.color_change(colors["white"])

                        self.__v_cells, self.__h_cells = new_size, new_size
                        self.__cell_size = int(min(board_height / self.__v_cells, board_width / self.__h_cells))
                        self.__board = Board(self.__v_cells, self.__h_cells, board_start[0], board_start[1],
                                             self.__cell_size, screen)
                        cells = self.__board.draw_board()

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

                        start_button.color_change(colors["green"])
                        maze_button.color_change(colors["white"])
                        maze_size_button.color_change(colors["white"])
                        draw_button.color_change(colors["white"])
                        erase_button.color_change(colors["white"])
                        reset_button.color_change(colors["yellow"])

                        self.reset_algorithms_colors()

                        reset_button()
                        self.__board.reset()

                        time.sleep(self.__TIME)

                    # Choosing Algorithm, Dijkstra
                    if dijkstra_button.rect.collidepoint(mouse):
                        if self.__ALGO != "Dijkstra":
                            self.__ALGO = "Dijkstra"

                            dijkstra_button.color_change(colors["yellow"])
                            astar_man_button.color_change(colors["white"])
                            astar_evk_button.color_change(colors["white"])

                            time.sleep(self.__TIME)
                        else:
                            self.__ALGO = None
                            self.reset_algorithms_colors()

                            time.sleep(self.__TIME)

                    # А* Manhattan
                    elif astar_man_button.rect.collidepoint(mouse):
                        if self.__ALGO != "AStarManhattan":
                            self.__ALGO = "AStarManhattan"

                            astar_man_button.color_change(colors["yellow"])
                            dijkstra_button.color_change(colors["white"])
                            astar_evk_button.color_change(colors["white"])

                            time.sleep(self.__TIME)
                        else:
                            self.__ALGO = None
                            self.reset_algorithms_colors()

                            time.sleep(self.__TIME)

                    # А* Euclidean
                    elif astar_evk_button.rect.collidepoint(mouse):
                        if self.__ALGO != "AStarEuclidean":
                            self.__ALGO = "AStarEuclidean"

                            astar_evk_button.color_change(colors["yellow"])
                            astar_man_button.color_change(colors["white"])
                            dijkstra_button.color_change(colors["white"])

                            time.sleep(self.__TIME)
                        else:
                            self.__ALGO = None
                            self.reset_algorithms_colors()

                            time.sleep(self.__TIME)

                    # Drawing and Erasing Logic
                    else:
                        for i in range(self.__v_cells):
                            for j in range(self.__h_cells):
                                cell = cells[i][j]
                                if (i, j) != self.__board.start or (i, j) != self.__board.target:
                                    if self.__DRAW and cell.collidepoint(mouse):
                                        self.__board.wall.add((i, j))
                                    elif self.__ERASE and cell.collidepoint(mouse) and (i, j) in self.__board.wall:
                                        self.__board.wall.remove((i, j))

                # Right-Button pressed(Erasing targets)
                elif right == 1:
                    mouse = pygame.mouse.get_pos()

                    for i in range(self.__v_cells):
                        for j in range(self.__h_cells):
                            if i < self.__v_cells and j < self.__h_cells:
                                cell = cells[i][j]
                                if cell.collidepoint(mouse):
                                    if (i, j) not in self.__board.wall and self.__board.start is None:
                                        self.__board.start = (i, j)
                                    elif (i, j) not in self.__board.wall and (
                                            i, j) != self.__board.start and self.__board.target is None:
                                        self.__board.target = (i, j)
                                    elif (i, j) == self.__board.start and self.__board.target is None:
                                        self.__board.start = None
                                    elif (i, j) == self.__board.target:
                                        self.__board.target = None

                    time.sleep(self.__TIME)
                pygame.display.flip()

            # Start Search
            else:
                if self.__board.start is None or self.__board.target is None:
                    print("Please choose position of START(target) and FINISH(target) to search")
                    self.__SEARCH = False
                    start_button.color_change(colors["green"])
                    continue
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

                    result_file.write("\nPath Found!\n")
                    result_file.write("Algorithm used: " + self.__ALGO + "\n")

                    state = self.__board.get_board_state()
                    result_file.write("1) Start: " + str(state["start"]) + "\n")
                    result_file.write("2) Target: " + str(state["target"]) + "\n")
                    result_file.write("3) Path: " + str(state["path"]) + "\n")

                    algorithm_info = algorithm.get_info()

                    Comparisons_info = "1)Comparisons: " + str(algorithm_info["comparisons"])
                    Comparisons.set_text("")
                    Comparisons.set_text(Comparisons_info)
                    Comparisons.draw(screen)

                    Iterations_info = "2)Iterations: " + str(algorithm_info["iterations"])
                    Iterations.set_text("")
                    Iterations.set_text(Iterations_info)
                    Iterations.draw(screen)

                    Visited_cells_info = "3)Visited Nodes: " + str(algorithm_info["visited_cells"])
                    Visited_cells.set_text("")
                    Visited_cells.set_text(Visited_cells_info)
                    Visited_cells.draw(screen)

                    Execution_time_info = "4)Execution time: " + str(algorithm_info["execution_time"])
                    Execution_time.set_text("")
                    Execution_time.set_text(Execution_time_info)
                    Execution_time.draw(screen)

                else:
                    print("Hmm, there is no solution..")

                    result_file.write("\nPath not Found!\n")
                    result_file.write("Algorithm used: " + self.__ALGO + "\n")

                    algorithm_info = algorithm.get_info()

                    Comparisons_info = "1)Comparisons: " + str(algorithm_info["comparisons"])
                    Comparisons.set_text("")
                    Comparisons.set_text(Comparisons_info)
                    Comparisons.draw(screen)

                    Iterations_info = "2)Iterations: " + str(algorithm_info["iterations"])
                    Iterations.set_text("")
                    Iterations.set_text(Iterations_info)
                    Iterations.draw(screen)

                    Visited_cells_info = "3)Visited Nodes: " + str(algorithm_info["visited_cells"])
                    Visited_cells.set_text("")
                    Visited_cells.set_text(Visited_cells_info)
                    Visited_cells.draw(screen)

                    Execution_time_info = "4)Execution time: " + str(algorithm_info["execution_time"])
                    Execution_time.set_text("")
                    Execution_time.set_text(Execution_time_info)
                    Execution_time.draw(screen)

                self.__SEARCH = False
                start_button.color_change(colors["green"])
        result_file.close()
    CLOCK.tick(FPS)
