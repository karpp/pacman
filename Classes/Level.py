from Classes.Image import *
import settings
import sys
import pygame


class Level:
    def __init__(self, screen):
        self.load_map(settings.maps_list[settings.level - 1])
        self.lives = [Image('images/big_pacman.png', 80 * i + 100, settings.window_height + settings.number_of_squares)
                      for i in range(3)]
        self.screen = screen

    def draw(self):  # прорисовка инфы

        myfont = pygame.font.SysFont("Calibri", 40)
        if self.check_alive():
            textsurface = myfont.render('Lives:', False, (255, 255, 255))
            self.screen.blit(textsurface, (0, settings.window_height + settings.number_of_squares))
            for live in self.lives:
                self.screen.blit(live.image, live.geometry)
        else:
            textsurface = myfont.render('GAME OVER', False, (255, 255, 255))
            self.screen.blit(textsurface, (settings.window_height // 3, settings.window_width // 3))
        if settings.level == 4:
            textsurface = myfont.render('YOU WON', False, (255, 255, 255))
            self.screen.fill([0, 0, 0])
            self.screen.blit(textsurface, (settings.window_height // 3, settings.window_width // 3))
            pygame.display.flip()
            pygame.time.wait(100)
            sys.exit()

    def collision(self):  # столкновение с гастом (потеря жизни)
        if len(self.lives) > 0:
            self.lives.pop()

    def load_map(self, file='sample.map'):  # загрузить карту
        pass

    def check_alive(self):
        return len(self.lives) > 0

    def check_food(self):
        pass
