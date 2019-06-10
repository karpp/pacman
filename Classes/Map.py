import pygame

import settings


class Map:
    def __init__(self):
        self.X = settings.number_of_squares
        self.Y = 3 * settings.number_of_squares
        if settings.window_width > settings.window_height:  # установка размера поля
            self.window_width = settings.window_height - 40
            while self.window_width % settings.number_of_squares != 0:
                self.window_width -= 1
        else:
            self.window_width = settings.window_height - 40
            while self.window_width % settings.number_of_squares != 0:
                self.window_width -= 1
        self.one_square = (self.window_width / settings.number_of_squares) - 1  # сторона  клетки
        self.walls = open(settings.maps_list[settings.level - 1],
                          'r').read()  # file - файл со знаками / и  &, отвечающими за стену или проход
        settings.map_x = self.X
        settings.map_y = self.Y
        settings.square = self.one_square
        k = 0
        j = 0
        for i in range(len(self.walls)):  # обработка шаблона карты
            if self.walls[i] == '/':
                settings.walls_on_map[k][j] = '/'
                if k == settings.number_of_squares - 1:
                    j += 1
                    k = 0
                else:
                    k += 1
            elif self.walls[i] == '&':
                settings.walls_on_map[k][j] = '&'
                if k == settings.number_of_squares - 1:
                    j += 1
                    k = 0
                else:
                    k += 1
            elif self.walls[i] == 'f':
                settings.walls_on_map[k][j] = 'Food'
                if k == settings.number_of_squares - 1:
                    j += 1
                    k = 0
                else:
                    k += 1
            elif self.walls[i] == 'c':
                settings.walls_on_map[k][j] = 'Cherry'
                if k == settings.number_of_squares - 1:
                    j += 1
                    k = 0
                else:
                    k += 1
            elif self.walls[i] == 'e':
                settings.walls_on_map[k][j] = 'Energizer'
                if k == settings.number_of_squares - 1:
                    j += 1
                    k = 0
                else:
                    k += 1
            elif self.walls[i] == 'd':
                settings.walls_on_map[k][j] = 'Door'
                if k == settings.number_of_squares - 1:
                    j += 1
                    k = 0
                else:
                    k += 1
            elif self.walls[i] == 'w':
                settings.walls_on_map[k][j] = 'Wall'
                if k == settings.number_of_squares - 1:
                    j += 1
                    k = 0
                else:
                    k += 1

    def food_draw(self, screen):
        for i in range(settings.number_of_squares):
            for j in range(settings.number_of_squares):
                if settings.walls_on_map[i][j] == 'Food':
                    a = pygame.Rect([i * self.one_square + self.X + self.one_square / 3,  # прорисовка еды
                                     j * self.one_square + self.Y + self.one_square / 3,
                                     float(self.one_square / 5), float(self.one_square / 5)])
                    pygame.draw.rect(screen, [255, 255, 255], a)
                if settings.walls_on_map[i][j] == 'Energizer':
                    a = pygame.Rect([i * self.one_square + self.X + self.one_square / 3,  # прорисовка еды
                                     j * self.one_square + self.Y + self.one_square / 3,
                                     float(self.one_square / 2.5), float(self.one_square / 2.5)])
                    pygame.draw.rect(screen, [255, 255, 255], a)
                if settings.walls_on_map[i][j] == "Cherry":
                    pass
                    # picture = pygame.image.load('images/cherry,png')

    def draw(self, screen):
        pygame.draw.line(screen, [255, 255, 0], (self.X - 1, self.Y - 1),
                         (1 + self.window_width, self.Y - 1))  # рисование границ карты желтым
        pygame.draw.line(screen, [255, 255, 0], (self.X - 1, self.Y - 1),
                         (self.X - 1, self.window_width + 2 * settings.number_of_squares))
        pygame.draw.line(screen, [255, 255, 0], (self.window_width, self.Y - 1),
                         (self.window_width, self.window_width + 2 * settings.number_of_squares))
        pygame.draw.line(screen, [255, 255, 0], (self.X - 1, 2 * settings.number_of_squares + self.window_width),
                         (self.window_width, 2 * settings.number_of_squares + self.window_width))
        for j in range(settings.number_of_squares):  # рисование самих стен. или красный квадрат или ничего не рисовать
            for k in range(settings.number_of_squares):
                r1 = pygame.Rect(
                    [j * self.one_square + self.X, k * self.one_square + self.Y, self.one_square, self.one_square])
                if settings.walls_on_map[j][k] == '/':
                    pygame.draw.rect(screen, [255, 0, 0], r1)
