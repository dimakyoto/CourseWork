import sys
from Constants import *
from Algorithms import *
from ShowElements import *
FREEZETIME = 0.1
pygame.init()

result_file = open("search_results.txt", "w")

#  Кнопки
start_button = RectButton(
    left=PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height = 1.5 * PADDING,
    text="Search Start", textcolor=colors["black"],
    rectcolor=colors["green"], screen=screen, font=RectButtonFont)

maze_button = RectButton(
    left=4.5 * PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height = 1.5 * PADDING,
    text="Maze", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

draw_button = RectButton(
    left=8 * PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height= 1.5 * PADDING,
    text="Draw Wall", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

erase_button = RectButton(
    left= 11.5 * PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height= 1.5 * PADDING,
    text="Erase Wall", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

reset_button = RectButton(
    left=15 * PADDING, top=HEIGHT - 2 * PADDING,
    width=3 * PADDING, height = 1.5 * PADDING,
    text="Reset", textcolor=colors["black"],
    rectcolor=colors["crimson"], screen=screen, font=RectButtonFont)

dijkstra_button = RectButton(
    left=17 * PADDING, top=3 * PADDING,
    width=3 * PADDING, height= 1.5 * PADDING,
    text="Dijkstra", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

astar_man_button = RectButton(
    left=17 * PADDING, top= 6 * PADDING,
    width=3 * PADDING, height= 1.5 * PADDING,
    text="A* (man)", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

astar_evk_button = RectButton(
    left=17 * PADDING, top= 9 * PADDING,
    width=3 * PADDING, height= 1.5 * PADDING,
    text="A* (evk)", textcolor=colors["black"],
    rectcolor=colors["white"], screen=screen, font=RectButtonFont)

#  Мейн-цикл
while RUNNING:
    # Вихід з проги
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    #  Бекграунд
    screen.fill(colors["black"])


    if not SEARCH:
        # Малюється дошка та отримуються координати клітинок на дошці, які використовуються для малювання та видалення стін.
        cells = board.draw_board()

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
        if RESET == True:
            time.sleep(0.05)
            reset_button.color_change(colors["crimson"])
            reset_button()
            RESET = False

            # Write the results to the file
            result_file.write("RESET pressed\n\n")

        # Натискання на мишу
        left, _, right = pygame.mouse.get_pressed()


        # Якщо ліва кнопка миші натиснута
        if left == 1:
            mouse = pygame.mouse.get_pos()

            # Кнопки модифікацій лабіринту

            # Кнопка старту
            if start_button.rect.collidepoint(mouse):
                if SEARCH == False:
                    SEARCH = True
                    DRAW = False
                    ERASE = False

                    draw_button.color_change(colors["white"])
                    erase_button.color_change(colors["white"])
                    start_button.color_change(colors["yellow"])

                    start_button()
                    draw_button()
                    erase_button()

                    time.sleep(FREEZETIME)

            # Кнопка рисування стін
            elif draw_button.rect.collidepoint(mouse):
                if  DRAW == False:
                    DRAW = True
                    ERASE = False
                    draw_button.color_change(colors["yellow"])
                    erase_button.color_change(colors["white"])
                else:
                    DRAW = False
                    draw_button.color_change(colors["white"])

                time.sleep(FREEZETIME)

                # Кнопка видалення стін
            elif erase_button.rect.collidepoint(mouse):
                if  ERASE == False:
                    ERASE = True
                    DRAW = False
                    erase_button.color_change(colors["yellow"])
                    draw_button.color_change(colors["white"])
                else:
                    ERASE = False
                    erase_button.color_change(colors["white"])

                time.sleep(FREEZETIME)

            # Кнопка RESET
            elif reset_button.rect.collidepoint(mouse):
                DRAW = False
                ERASE = False
                RESET = True

                draw_button.color_change(colors["white"])
                erase_button.color_change(colors["white"])
                reset_button.color_change(colors["yellow"])

                reset_button()
                board.reset()

                time.sleep(FREEZETIME)

                # Кнопка генерації лабіринту
            elif maze_button.rect.collidepoint(mouse):
                if board.wall:
                    print("Please press RESET(button) to reset the Board")
                    time.sleep(FREEZETIME)
                    continue

                if not board.start:
                    print("Please select START(target) to generate MAZE")
                    time.sleep(FREEZETIME)
                    continue

                elif board.target:
                    print("Please do not set FINISH(target), you need just to select start target and than you can generate maze")
                    time.sleep(FREEZETIME)
                    continue

                DRAW = False
                ERASE = False
                draw_button.color_change(colors["white"])
                erase_button.color_change(colors["white"])
                maze_button.color_change(colors["yellow"])

                maze_button()

                maze_creator = Maze(board)
                maze_creator.initialize()
                maze_creator.generate()

                maze_button.color_change(colors["white"])
                maze_button()

                time.sleep(FREEZETIME)


            # Кнопки вибору алгоритмів

            # Дейкстра
            if dijkstra_button.rect.collidepoint(mouse):
                ALGO = "Dijkstra"

                dijkstra_button.color_change(colors["yellow"])
                astar_man_button.color_change(colors["white"])
                astar_evk_button.color_change(colors["white"])

                time.sleep(FREEZETIME)


            # А* манхетенська
            elif astar_man_button.rect.collidepoint(mouse):
                ALGO = "AStar_man"

                astar_man_button.color_change(colors["yellow"])
                dijkstra_button.color_change(colors["white"])
                astar_evk_button.color_change(colors["white"])

                time.sleep(FREEZETIME)

                # А* евклідова
            elif astar_evk_button.rect.collidepoint(mouse):
                ALGO = "AStar_evk"

                astar_evk_button.color_change(colors["yellow"])
                astar_man_button.color_change(colors["white"])
                dijkstra_button.color_change(colors["white"])


                time.sleep(FREEZETIME)

            # Малювання або стирання стіни
            else:
                for i in range(v_cells):
                    for j in range(h_cells):
                        cell = cells[i][j]
                        if (i, j) != board.start or (i, j) != board.target:
                            if DRAW and cell.collidepoint(mouse):
                                board.wall.add((i, j))
                            elif ERASE and cell.collidepoint(mouse) and (i, j) in board.wall:
                                board.wall.remove((i, j))

        # Натискання на праву кнопку, стирання старту або фінішу
        elif right == 1:
            mouse = pygame.mouse.get_pos()

            for i in range(v_cells):
                for j in range(h_cells):
                    cell = cells[i][j]
                    if cell.collidepoint(mouse):
                        # if it's not wall and start has not been created, create start
                        if (i, j) not in board.wall and board.start is None:
                            board.start = (i, j)
                        # if it's not wall and start, and target has not been created, create target
                        elif (i, j) not in board.wall and (i, j) != board.start and board.target is None:
                            board.target = (i, j)
                        # if it's start and target has not been created, chancel start
                        elif (i, j) == board.start and board.target is None:
                            board.start = None
                        # if it's target, chancel target
                        elif (i, j) == board.target:
                            board.target = None

            time.sleep(FREEZETIME)

        pygame.display.flip()


    # Початок пошуку
    else:
        # Якщо нема старту і кінця кіна не буде аххахаххаа
        if board.start is None or board.target is None:
            print("Please choose position of START(target) and FINISH(target)")
            SEARCH = False
            start_button.color_change(colors["green"])
            continue

            # Не обрав алгоритм
        elif ALGO is None:
            print("Please choose algorithm")
            SEARCH = False
            start_button.color_change(colors["green"])
            continue

        if board.visited or board.path:
            board.clear_visited()

        # Застосування обраного алгоритму
        if ALGO == "Dijkstra":
            algorithm = Dijkstra(board)
            algorithm.make_info()
            algorithm.finding_path()


        elif ALGO == "AStar_man":
            algorithm = AStar_man(board)
            algorithm. make_info()
            algorithm.finding_path()


        elif ALGO == "AStar_evk":
            algorithm = AStar_evk(board)
            algorithm.make_info()
            algorithm.finding_path()

        # Якщо дорога знайдена
        if algorithm.find == True:
            algorithm.output()

            # Write the results to the file
            result_file.write("Path Found!\n")
            result_file.write("Algorithm used: " + ALGO + "\n")

            state = board.get_board_state()
            result_file.write("1)Start: " + str(state["start"]) + "\n")
            result_file.write("2)Target: " + str(state["target"]) + "\n")
            result_file.write("3)Path: " + str(state["path"]) + "\n")

        else:
            print("Hmm, there is no solution..")

            result_file.write("Path not Found!\n")
            result_file.write("Algorithm used: " + ALGO + "\n")

        # Рестарт гри
        SEARCH = False
        start_button.color_change(colors["green"])

result_file.close()
CLOCK.tick(FPS)