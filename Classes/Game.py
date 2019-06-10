
from Classes.Ghost import *
from Classes.Level import *
from Classes.Map import *
from Classes.Menu import *
from Classes.Recordes import *


class Game:
    def __init__(self):
        self.speed = settings.current_speed
        self.background_colour = (0, 0, 0)
        self.display = (settings.window_height, settings.window_width)

    def play(self, screen, start_time):
        # Создаем окошко
        pygame.display.set_caption("Pacman")  # Пишем в шапку
        pygame.font.init()
        level = Level(screen)
        w_close = False
        game_map = Map()
        pacman = Pacman(200, 200, screen)
        score = Button((settings.window_height / 6, rect_height // 2), rect_height, rect_width, "Рекорды")
        pause = Button((settings.window_height / 6 + rect_width, rect_height // 2), rect_height, rect_width, "Пауза")
        finish = Button((settings.window_height / 6 + 2 * rect_width, rect_height // 2), rect_height, rect_width,
                        "Главное меню")
        time = Button((settings.window_height / 2, rect_height * 1.5), rect_height, settings.window_height,
                      "0000")
        pause_colour = red
        score_colour = red
        finish_colour = red
        time_colour = bg_color
        pacman.set_pos(1, 2)
        clyde = Clyde(12, 14)
        blinky = Blinky(12, 12)
        inky = Inky(15, 14)
        pinky = Pinky(15, 12)
        while not w_close:
            right_time = pygame.time.get_ticks()
            # --- обработка событий ---
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    w_close = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if pause.is_on_button(pos[0], pos[1]):
                        w_close = func_pause(pause, score, finish, screen)
                        start_time += pygame.time.get_ticks() - right_time
                    if score.is_on_button(pos[0], pos[1]):
                        rec(screen)
                        start_time += pygame.time.get_ticks() - right_time
                    if finish.is_on_button(pos[0], pos[1]):
                        if yes_no(screen):
                            return False
                        start_time += pygame.time.get_ticks() - right_time
                if event.type == pygame.KEYDOWN:
                    pacman.move(event.key)
                    pacman.remember(event.key)

                if pause.is_on_button(pos[0], pos[1]):
                    pause_colour = pr_red
                else:
                    pause_colour = red

                if score.is_on_button(pos[0], pos[1]):
                    score_colour = pr_red
                else:
                    score_colour = red

                if finish.is_on_button(pos[0], pos[1]):
                    finish_colour = pr_red
                else:
                    finish_colour = red
            right_time = pygame.time.get_ticks()
            # --- отрисовка картинки ---
            screen.fill(self.background_colour)
            game_map.draw(screen)
            level.draw()
            game_map.food_draw(screen)
            pacman.step()
            time.change_text(str((right_time - start_time) // 100 / 10))
            time.draw(time_colour, screen)
            pause.draw(pause_colour, screen)
            score.draw(score_colour, screen)
            finish.draw(finish_colour, screen)
            food_left = False
            for i in range(
                    settings.number_of_squares):  # проверка съедена ли вся еда. если да - то переход на след уровень
                for j in range(settings.number_of_squares):
                    if settings.walls_on_map[i][j] == 'Energizer' or settings.walls_on_map[i][j] == "Food":
                        food_left = True
            if not food_left:
                name = new_record(screen)
                edit_record(name, str((right_time - start_time) // 1000), settings.level, screen)
                settings.level += 1
                level.draw()
                self.play(screen, pygame.time.get_ticks())
                return False

            if Pacman.ate_energizer:
                blinky.panic()
                pinky.panic()
                inky.panic()
                clyde.panic()
                Pacman.ate_energizer = False

            # проверка на столкновение
            if Ghost.collision and clock() - pacman.death_time > 2:
                Ghost.collision = False
                level.collision()
                pacman.pacman_dies()
                if not level.check_alive():
                    return

            # Ghost
            pinky.step()
            inky.step()
            blinky.step()
            clyde.step()

            screen.blit(pacman.rotated_pic, pacman.geometry)

            # Ghost
            screen.blit(pinky.ghost_pic, pinky.geometry)
            screen.blit(inky.ghost_pic, inky.geometry)
            screen.blit(blinky.ghost_pic, blinky.geometry)
            screen.blit(clyde.ghost_pic, clyde.geometry)

            pygame.display.flip()
            pygame.time.wait(10)
        sys.exit()
