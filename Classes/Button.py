import pygame

import settings

black = (0, 0, 0)
grey = (40, 40, 40)
pr_red = (200, 0, 0)
bg_color = black
red = (255, 0, 0)
yellow = (255, 255, 0)
rect_width = settings.window_height / 3
rect_height = 40
font_height = 20
white = (255,255,255)


class Button:
    def __init__(self, center, height, width, text):
        self.center = center
        self.height = height
        self.width = width
        self.text = text

    def is_on_button(self, x, y):
        if self.center[0] - self.width / 2 <= x <= self.center[0] + self.width / 2:
            if self.center[1] - self.height / 2 <= y <= self.center[1] + self.height / 2:
                return True
        return False

    def draw(self, colour, screen):
        pygame.draw.rect(screen, colour,
                         (self.center[0] - self.width / 2, self.center[1] - self.height / 2, self.width, self.height))
        font = pygame.font.Font('freesansbold.ttf', 20)
        text_surf = font.render(self.text, True, yellow, colour)
        text_rect = text_surf.get_rect()
        text_rect.center = self.center
        screen.blit(text_surf, text_rect)

    def change_text(self, text):
        self.text = text
