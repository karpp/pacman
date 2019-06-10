from Classes.Recordes import *


def func_pause(pause, score, finish, screen):
    is_pause = True
    while is_pause:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                if pause.is_on_button(pos[0], pos[1]):
                    return False

                if finish.is_on_button(pos[0], pos[1]):
                    return True
                if score.is_on_button(pos[0], pos[1]):
                    rec(screen)

            if event.type == pygame.QUIT:
                return True

            pause_colour = pr_red

            if score.is_on_button(pos[0], pos[1]):
                score_colour = pr_red
            else:
                score_colour = red

            if finish.is_on_button(pos[0], pos[1]):
                finish_colour = pr_red
            else:
                finish_colour = red

            pause.draw(pause_colour, screen)
            score.draw(score_colour, screen)
            finish.draw(finish_colour, screen)
            pygame.display.flip()
            pygame.time.wait(10)


def yes_no(screen):
    w_close = False
    pygame.display.set_caption("Pacman")  # Пишем в шапку
    question = Button((settings.window_height / 2, settings.window_width / 4), 2 * rect_height, window_height,
                      "Вы хотите покинуть игру?")
    yes = Button((settings.window_height / 4, settings.window_width / 2), 2 * rect_height, rect_width, "Да")
    no = Button((settings.window_height * 0.75, settings.window_width / 2), 2 * rect_height, rect_width, "Нет")
    yes_colour = red
    no_colour = red
    question_colour = red
    while not w_close:
        # --- обработка событий ---
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                w_close = True
            if event.type == pygame.MOUSEBUTTONUP:
                if yes.is_on_button(pos[0], pos[1]):
                    return yes
                if no.is_on_button(pos[0], pos[1]):
                    return False
            if event.type == pygame.QUIT:
                sys.exit()
            if yes.is_on_button(pos[0], pos[1]):
                yes_colour = pr_red
            else:
                yes_colour = red

            if no.is_on_button(pos[0], pos[1]):
                no_colour = pr_red
            else:
                no_colour = red

        # --- отрисовка картинки ---

        screen.fill(bg_color)
        question.draw(question_colour, screen)
        yes.draw(yes_colour, screen)
        no.draw(no_colour, screen)
        pygame.display.flip()
        pygame.time.wait(10)


class Menu:
    def __init__(self):
        self.background_colour = (0, 0, 0)
        self.display = (settings.window_height, settings.window_width)

    def open_menu(self, screen):
        w_close = False
        pygame.display.set_caption("Pacman")  # Пишем в шапку
        title_button = Button((settings.window_height / 2, settings.window_width / 6), 2 * rect_height,
                              settings.window_height, "PACMAN")
        start_button = Button((settings.window_height / 2, settings.window_width / 3), 2 * rect_height, rect_width,
                              "Начать игру")
        records_button = Button((settings.window_height / 2, settings.window_width / 3 * 2 - settings.window_width / 6),
                                2 * rect_height, rect_width, "Рекорды")
        quit_button = Button((settings.window_height / 2, settings.window_width / 3 * 2), 2 * rect_height, rect_width,
                             "Выйти")
        recordes_colour = red
        start_colour = red
        quit_colour = red

        while not w_close:
            # --- обработка событий ---
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    w_close = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if records_button.is_on_button(pos[0], pos[1]):
                        rec(screen)
                    if start_button.is_on_button(pos[0], pos[1]):
                        w_close = True
                    if quit_button.is_on_button(pos[0], pos[1]):
                        sys.exit()
                if event.type == pygame.QUIT:
                    sys.exit()
                if records_button.is_on_button(pos[0], pos[1]):
                    recordes_colour = pr_red
                else:
                    recordes_colour = red

                if start_button.is_on_button(pos[0], pos[1]):
                    start_colour = pr_red
                else:
                    start_colour = red

                if quit_button.is_on_button(pos[0], pos[1]):
                    quit_colour = pr_red
                else:
                    quit_colour = red

            # --- отрисовка картинки ---

            screen.fill(self.background_colour)
            title_button.draw(red, screen)
            records_button.draw(recordes_colour, screen)
            quit_button.draw(quit_colour, screen)
            start_button.draw(start_colour, screen)
            pygame.display.flip()
            pygame.time.wait(10)

    def level_menu(self, screen):
        w_close = False
        pygame.display.set_caption("Pacman")  # Пишем в шапку
        title = Button((settings.window_height / 2, settings.window_width / 6), 2 * rect_height, settings.window_height,
                       "PACMAN")
        level1 = Button((settings.window_height / 2, settings.window_width / 3), 2 * rect_height, rect_width,
                        "Уровень 1")
        level2 = Button((settings.window_height / 2, settings.window_width / 3 * 2 - settings.window_width / 6),
                        2 * rect_height, rect_width,
                        "Уровень 2")
        level3 = Button((settings.window_height / 2, settings.window_width / 3 * 2), 2 * rect_height, rect_width,
                        "Уровень 3")
        back = Button((settings.window_height / 2, settings.window_width / 3 * 2 + settings.window_width / 6),
                      2 * rect_height, rect_width,
                      "Главное меню")
        level1_colour = red
        level2_colour = red
        level3_colour = red
        back_colour = red
        while not w_close:
            # --- обработка событий ---
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    w_close = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if level1.is_on_button(pos[0], pos[1]):
                        return 1
                    if level2.is_on_button(pos[0], pos[1]):
                        return 2
                    if level3.is_on_button(pos[0], pos[1]):
                        return 3
                    if back.is_on_button(pos[0], pos[1]):
                        return 4
                if event.type == pygame.QUIT:
                    sys.exit()
                if level1.is_on_button(pos[0], pos[1]):
                    level1_colour = pr_red
                else:
                    level1_colour = red

                if level2.is_on_button(pos[0], pos[1]):
                    level2_colour = pr_red
                else:
                    level2_colour = red

                if level3.is_on_button(pos[0], pos[1]):
                    level3_colour = pr_red
                else:
                    level3_colour = red

                if back.is_on_button(pos[0], pos[1]):
                    back_colour = pr_red
                else:
                    back_colour = red

            # --- отрисовка картинки ---

            screen.fill(self.background_colour)
            title.draw(red, screen)
            level1.draw(level1_colour, screen)
            level2.draw(level2_colour, screen)
            level3.draw(level3_colour, screen)
            back.draw(back_colour, screen)
            pygame.display.flip()
            pygame.time.wait(10)
