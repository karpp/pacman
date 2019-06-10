from Classes.Button import *
import sys
window_height = settings.window_height
window_width = settings.window_width
import pygame

class Record:
    def __init__(self, center, height, txt, numb):
        self.center = (center[0], center[1] - height / 12 + height / 6 * (numb - 3))
        self.txt = txt

    def draw(self, txt_clr, back_clr, screen, title):
        font = pygame.font.Font('freesansbold.ttf', 13 + 10 * title)
        text_surf = font.render(self.txt, True, txt_clr, back_clr)
        text_rect = text_surf.get_rect()
        text_rect.center = self.center
        screen.blit(text_surf, text_rect)


class Recordes:
    def __init__(self, lev, center, height, width):
        self.lev = lev
        self.names = ['-'] * 5
        self.scores = [0] * 5
        self.height = height
        self.width = width
        self.center = center
        file = open(settings.recordes_list[lev - 1], "r")
        for i in range(0, 5):
            self.names[i] = file.readline()
            self.scores[i] = file.readline()
            self.names[i] = self.names[i][0:-1]
            self.scores[i] = self.scores[i][0:-1]

    def draw(self, txt_clr, back_clr, screen):
        pygame.draw.rect(screen, back_clr,
                         (self.center[0] - self.width / 2, self.center[1] - self.height / 2, self.width, self.height))
        Record(self.center, self.height, "LEVEL" + str(self.lev), 1).draw(txt_clr, back_clr, screen, 1)
        Record(self.center, self.height, self.names[0] + " " + str(self.scores[0]), 2).draw(txt_clr, back_clr, screen,
                                                                                            0)
        Record(self.center, self.height, self.names[1] + " " + str(self.scores[1]), 3).draw(txt_clr, back_clr, screen,
                                                                                            0)
        Record(self.center, self.height, self.names[2] + " " + str(self.scores[2]), 4).draw(txt_clr, back_clr, screen,
                                                                                            0)
        Record(self.center, self.height, self.names[3] + " " + str(self.scores[3]), 5).draw(txt_clr, back_clr, screen,
                                                                                            0)
        Record(self.center, self.height, self.names[4] + " " + str(self.scores[4]), 6).draw(txt_clr, back_clr, screen,
                                                                                            0)

def rec(screen):
    w_close = False
    quit_button = Button((window_height / 2, rect_height / 2), rect_height, window_height, "Продолжить")
    quit_colour = black
    while not w_close:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if quit_button.is_on_button(pos[0], pos[1]):
                    w_close = True
            if quit_button.is_on_button(pos[0], pos[1]):
                quit_colour = grey
            else:
                quit_colour = black
        quit_button.draw(quit_colour, screen)
        Recordes(1, (window_height / 2, (window_width - rect_height) / 6 + rect_height),
                 (window_width - rect_height) / 3,
                 window_height).draw(yellow, red, screen)
        Recordes(2, (window_height / 2, (window_width - rect_height) / 2 + rect_height),
                 (window_width - rect_height) / 3,
                 window_height).draw(red, yellow, screen)
        Recordes(3, (window_height / 2, (window_width - rect_height) / 6 * 5 + rect_height),
                 (window_width - rect_height) / 3,
                 window_height).draw(yellow, red, screen)
        pygame.display.flip()
        pygame.time.wait(10)

def new_record(screen):
    screen.fill(black)
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(window_width/4, window_height/2, 200, 32)
    color_inactive = pygame.Color('yellow')
    color_active = pygame.Color('red')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(black)
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        fontAddBall = pygame.font.Font('freesansbold.ttf', 30)
        textSurfAddBall = fontAddBall.render("Имя для таблицы рекордов", True, yellow, black)
        textRectAddBall = textSurfAddBall.get_rect()
        textRectAddBall.center = (window_height/2, window_width/4)
        screen.blit(textSurfAddBall, textRectAddBall)

        pygame.display.flip()
        clock.tick(30)

def edit_record(Nick, Time, lev, screen):
    names = ['-'] * 5
    scores = [0] * 5
    Time = int(Time)
    file = open(settings.recordes_list[lev - 1], "r")
    for i in range(0, 5):
        names[i] = file.readline()
        scores[i] = file.readline()
        names[i] = names[i][0:-1]
        scores[i] = scores[i][0:-1]
        scores[i] = int(scores[i])
    file.close()
    file = open(settings.recordes_list[lev - 1], "w+")
    for i in range(0, 5):
        if Time <= scores[i]:
            t = Time
            Time = scores[i]
            scores[i] = t
            n = Nick
            Nick = names[i]
            names[i] = n
        file.write(names[i])
        file.write("\n")
        file.write(str(scores[i]))
        file.write("\n")
    file.close()
    rec(screen)