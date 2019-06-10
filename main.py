import pygame
from Classes import Menu
from Classes import Game
import settings

close = False
pygame.init()
screen = pygame.display.set_mode((settings.window_height, settings.window_width))
while not close:
    settings.level = 4
    while settings.level == 4:
        Menu.Menu().open_menu(screen)
        settings.level = Menu.Menu().level_menu(screen)
    close = Game.Game().play(screen, pygame.time.get_ticks())
