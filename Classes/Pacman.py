import sys
from time import clock
from Classes.Button import*
import pygame

import settings


class Pacman:
    x, y = 0, 0  # для работы гостов
    go = [0, 0]  # это тоже
    ate_energizer = False

    def __init__(self, x, y, screen):
        self.speed = settings.current_speed
        self.screen = screen
        self.align = [0, 0]
        # Всего 4 направления движения.
        # Регулируется с помощью стрелочек в правом нижнем углу клавиатуры.
        # При нажатии одной кнопки Пакмен начинает двигаться без остановки,
        # как и в оригинале игры.
        # С начала игры движется влево.
        self.pacman_pic = pygame.image.load('images/core_pacman.png')
        self.rotated_pic = pygame.transform.rotate(self.pacman_pic, 180)
        # Пока что картинка, в будущем, надеюсь, объект pygame.

        self.points = 0  # Счётчик очков.
        self.geometry = self.pacman_pic.get_rect()  # Подключаем геометрию.

        self.geometry.x = x
        self.geometry.y = y

        self.key = None
        self.death_time = -10

        self.ceilx = 0
        self.ceily = 0
        self.find_ceil()
        self.remembered = False

        self.life = 3  # Три жизни

    def acceleration(self):  # В разработке, ожидает обсуждения с тимлидом.
        pass

    def slowdown(self):  # В разработке, ожидает обсуждения с тимлидом.
        pass

    @staticmethod
    def move(key):
        if key == 27:
            sys.exit()

    def pacman_dies(self):
        self.life -= 1
        self.death_time = clock()
        self.set_pos(1, 1)
        Pacman.x = Pacman.y = len(settings.walls_on_map) // 2
        if self.life == 0:
            animation_of_death(self.screen)  # будет написано
            # end_this_game()  # тоже будет написано

    # Функция изменения направления
    def change_direction(self, key):
        # на всякий случай, запомнить, что было до функции
        prev_rotated_pic = self.rotated_pic
        prev_align = self.align

        if key == 273 and self.geometry.top > 0:  # up
            self.rotated_pic = pygame.transform.rotate(self.pacman_pic, 90)
            self.align = [0, -self.speed]
        elif key == 274 and self.geometry.bottom < settings.window_height:  # down
            self.rotated_pic = pygame.transform.rotate(self.pacman_pic, 270)
            self.align = [0, self.speed]
        elif key == 275 and self.geometry.right < settings.window_width:  # right
            self.rotated_pic = pygame.transform.rotate(self.pacman_pic, 0)
            self.align = [self.speed, 0]
        elif key == 276 and self.geometry.left > 0:  # left
            self.rotated_pic = pygame.transform.rotate(self.pacman_pic, 180)
            self.align = [-self.speed, 0]

        # если я иду в стену, то надо бы остановиться
        move = [self.align[0] // self.speed, self.align[1] // self.speed]
        if settings.walls_on_map[self.ceilx + move[0]][self.ceily + move[1]] == '/' or \
                        settings.walls_on_map[self.ceilx + move[0]][self.ceily + move[1]] == 'Door' or \
                        settings.walls_on_map[self.ceilx + move[0]][self.ceily + move[1]] == 'Wall':
            self.align = prev_align
            self.rotated_pic = prev_rotated_pic

        # если все ок, можно забыть, что меня просили повернуть
        else:
            self.remembered = False

    def step(self):
        if clock() - self.death_time <= 2:
            return

        # запустить проверку, не стоит ли pacman посередине клетки
        self.find_ceil()
        self.geometry = self.geometry.move(self.align)

        # Эта функция не даёт уйти нашему пакмену за пределы карты
        if self.geometry.left <= 0 and self.align == [-self.speed, 0]:
            self.align = [0, 0]
        if self.geometry.right >= settings.window_width and self.align == [self.speed, 0]:
            self.align = [0, 0]
        if self.geometry.top <= 0 and self.align == [0, -self.speed]:
            self.align = [0, 0]
        if self.geometry.bottom >= settings.window_height + 20 and self.align == [0, self.speed]:
            self.align = [0, 0]

    def find_ceil(self):
        # определить координаты клетки, в которой находится pacman
        Pacman.x = self.ceilx = int((self.geometry.x - settings.map_x) // settings.square)
        Pacman.y = self.ceily = int((self.geometry.y - settings.map_y) // settings.square)

        # если pacman находится в радиусе 3 от центра клетки, подумать
        if (self.geometry.x - settings.map_x) % settings.square < 3 and (
                    self.geometry.y - settings.map_y) % settings.square < 3:
            self.think()

    def think(self):
        if settings.walls_on_map[self.ceilx][self.ceily] == 'Food':
            settings.walls_on_map[self.ceilx][self.ceily] = '&'
            # добавить очки

        elif settings.walls_on_map[self.ceilx][self.ceily] == 'Energizer':
            settings.walls_on_map[self.ceilx][self.ceily] = '&'
            Pacman.ate_energizer = True

        elif settings.walls_on_map[self.ceilx][self.ceily] == 'Cherry':
            settings.walls_on_map[self.ceilx][self.ceily] = '&'
            # добавить очки

        # вспомнить, не просили ли меня повернуть
        if self.remembered:
            self.change_direction(self.key)

        # определить, куда я собираюсь идти
        Pacman.go = move = [self.align[0] // self.speed, self.align[1] // self.speed]

        # если я иду в стену, то надо бы остановиться
        if settings.walls_on_map[self.ceilx + move[0]][self.ceily + move[1]] == '/':
            self.align = [0, 0]

    def set_pos(self, ceilx, ceily):
        # поставить себя в середину клетки с координатами (x, y)

        self.geometry.x = settings.map_x + ceilx * settings.square
        self.geometry.y = settings.map_y + ceily * settings.square
        self.find_ceil()

    def remember(self, key):
        # запомнить, что меня просили повернуть
        self.remembered = True
        self.key = key


def animation_of_death(screen):
    w_close = False
    pygame.display.set_caption("Pacman")  # Пишем в шапку
    game_over = Button((settings.window_height / 2, settings.window_width / 4), 3 * rect_height, settings.window_height,
                      "GAME OVER")
    ok = Button((settings.window_height / 2, settings.window_width / 4 * 2), 2 * rect_height, settings.window_height/3,
                      "OK")
    game_colour = red
    ok_colour = red
    while not w_close:
        # --- обработка событий ---
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if ok.is_on_button(pos[0], pos[1]):
                    w_close = True
            if event.type == pygame.QUIT:
                sys.exit()
            if ok.is_on_button(pos[0], pos[1]):
                ok_colour = pr_red
            else:
                ok_colour = red

        # --- отрисовка картинки ---

        screen.fill((0,0,0))
        game_over.draw(game_colour, screen)
        ok.draw(ok_colour, screen)
        pygame.display.flip()
        pygame.time.wait(10)