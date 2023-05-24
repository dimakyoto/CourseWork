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
        self.__board = Board(self.__v_cells, self.__h_cells, board_start[0], board_start[1], self.__cell_size, screen,
                             colors)

    def input_field(self):
        input_box = pygame.Rect(225, 285, 100, 32)
        color_inactive = pygame.Color(colors["deepskyblue"])
        color_active = pygame.Color(colors["blue"])

        color = color_inactive
        active = False
        text = ''

        instruction_font = pygame.font.SysFont("timesnewroman", 24)
        instruction_text = instruction_font.render("Enter size of the maze (f.e. 30): ", True, (colors["black"]))
        instruction_text_rect = instruction_text.get_rect(center=(WIDTH // 2, 250))

        ps_text_font = pygame.font.SysFont("timesnewroman", 20)
        ps_text = ps_text_font.render("Warning, the input number must be lower or equal to 50!!!", True,
                                      colors["crimson"])
        ps_text_rect = ps_text.get_rect(bottomleft=(10, HEIGHT - 10))

        cursor_color = pygame.Color("black")
        cursor_visible = True
        cursor_timer = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                    if back_button.rect.collidepoint(event.pos):
                        return
                if event.type == KEYDOWN:
                    if active:
                        if event.key == K_RETURN:
                            return int(text)
                        elif event.key == K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            screen.fill((colors["gainsboro"]))
            txt_surface = RectButtonFont.render(text, True, colors["black"])
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width

            screen.blit(instruction_text, instruction_text_rect)
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)
            screen.blit(ps_text, ps_text_rect)

            # Мигающий курсор
            if active:
                cursor_timer += CLOCK.get_time()
                if cursor_timer >= 500:
                    cursor_visible = not cursor_visible
                    cursor_timer = 0

            if cursor_visible and active:
                cursor_pos = (input_box.x + txt_surface.get_width() + 10, input_box.y + 10)
                pygame.draw.line(screen, cursor_color, cursor_pos,
                                 (cursor_pos[0], cursor_pos[1] + input_box.height - 20), 2)
            back_button()
            pygame.display.flip()
            CLOCK.tick(FPS)

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
                maze_size_button()

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

                    # SIZE-Button
                    elif maze_size_button.rect.collidepoint(mouse):

                        if self.__board.wall:
                            print("Please press RESET(button) to reset the Board")
                            time.sleep(self.__TIME)
                            continue

                        self.__DRAW = False
                        self.__ERASE = False
                        draw_button.color_change(colors["white"])
                        erase_button.color_change(colors["white"])
                        maze_button.color_change(colors["white"])
                        maze_button.color_change(colors["white"])
                        maze_size_button.color_change(colors["yellow"])

                        new_size = self.input_field()

                        if new_size is None:
                            # User canceled the input, handle it accordingly
                            maze_size_button.color_change(colors["white"])
                            continue

                        if new_size > 50:
                            print("Please enter a size less than or equal to 50")
                            time.sleep(self.__TIME)
                            continue

                        maze_size_button.color_change(colors["white"])

                        self.__v_cells, self.__h_cells = new_size, new_size
                        self.__cell_size = int(min(board_height / self.__v_cells, board_width / self.__h_cells))
                        self.__board = Board(self.__v_cells, self.__h_cells, board_start[0], board_start[1],
                                             self.__cell_size, screen,
                                             colors)
                        cells = self.__board.draw_board()

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
                            dijkstra_button.color_change(colors["white"])
                            astar_man_button.color_change(colors["white"])
                            astar_evk_button.color_change(colors["white"])

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
                            astar_man_button.color_change(colors["white"])
                            dijkstra_button.color_change(colors["white"])
                            astar_evk_button.color_change(colors["white"])

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
                            astar_evk_button.color_change(colors["white"])
                            astar_man_button.color_change(colors["white"])
                            dijkstra_button.color_change(colors["white"])

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
