import pygame


class Image:
    def __init__(self, img, x, y):
        self.image = pygame.image.load(img)
        self.geometry = self.image.get_rect()
        self.set_pos(x, y)

    def set_pos(self, x, y):
        self.geometry.x = x
        self.geometry.y = y
