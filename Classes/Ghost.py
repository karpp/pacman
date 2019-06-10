from random import choice

from Classes.Pacman import *


class Ghost:
    collision = False

    def __init__(self, x, y, pic, debug=False):
        self.align = [0, 0]
        self.speed = settings.current_speed - 1

        self.ghost_pic = pygame.image.load(pic)
        self.scared_pic = pygame.image.load('images/ghost_scared.png')
        self.geometry = self.ghost_pic.get_rect()

        self.direction = 0
        # 0 - up, 1 - right, 2 - down, 3 - left

        self.attack = True
        # False, если Pac-Man съел большую точку

        self.ceilx = 0
        self.ceily = 0
        self.targetx = 0
        self.targety = 0
        self.nextx = 0
        self.nexty = 0
        self.debug = debug

        self.startx = x
        self.starty = y
        self.killed_time = clock()
        self.panic_time = -10

        self.align = [0, 0]

        self.set_pos(x, y)
        self.target()

        self.think()
        self.set_align()

        self.find_ceil()

    def step(self):
        self.find_ceil()

        self.geometry = self.geometry.move(self.align)

        if not self.attack and clock() - self.panic_time >= settings.energizer_time:
            self.end_panic()

        if self.ceilx == Pacman.x and self.ceily == Pacman.y:
            if self.attack:
                Ghost.collision = True
            else:
                self.end_panic()
                self.kill()

    def set_pos(self, ceilx, ceily):
        self.geometry.y = settings.map_y + ceily * settings.square
        self.geometry.x = settings.map_x + ceilx * settings.square
        self.geometry.y = settings.map_y + ceily * settings.square
        self.find_ceil()

    def find_ceil(self):
        self.ceilx = int((self.geometry.x - settings.map_x) // settings.square)
        self.ceily = int((self.geometry.y - settings.map_y) // settings.square)

        if (self.geometry.x - settings.map_x) % settings.square == 0 and (
                    self.geometry.y - settings.map_y) % settings.square == 0:
            self.think()

    def set_align(self):
        if self.direction == 1:
            self.align = [self.speed, 0]
        elif self.direction == 3:
            self.align = [-self.speed, 0]
        elif self.direction == 2:
            self.align = [0, self.speed]
        elif self.direction == 0:
            self.align = [0, -self.speed]
        else:
            # Well, this shouldn't happen...
            pass

        if clock() - self.killed_time < 3:
            self.align = [0, 0]

    def check(self):
        moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        self.nextx = self.ceilx + moves[self.direction][0]
        self.nexty = self.ceily + moves[self.direction][1]

        return settings.walls_on_map[self.ceilx + moves[self.direction][0]][
                   self.ceily + moves[self.direction][1]] != '/' and \
               settings.walls_on_map[self.ceilx + moves[self.direction][0]][
                   self.ceily + moves[self.direction][1]] != 'Wall' and \
               (settings.walls_on_map[self.ceilx + moves[self.direction][0]][
                    self.ceily + moves[self.direction][1]] != 'Door' or self.direction == 0)

    def dist_to_target(self):
        return (self.nextx - self.targetx) ** 2 + (self.nexty - self.targety) ** 2

    def think(self):
        next_move = []

        m = len(settings.walls_on_map) ** 3
        self.check()
        self.target()

        if self.check():
            if self.dist_to_target() == m:
                next_move.append(self.direction)
            elif self.dist_to_target() < m:
                next_move = [self.direction]
                m = self.dist_to_target()

        self.direction = (self.direction + 1) % 4

        if self.check():
            if self.dist_to_target() == m:
                next_move.append(self.direction)
            elif self.dist_to_target() < m:
                next_move = [self.direction]
                m = self.dist_to_target()

        self.direction = (self.direction + 2) % 4

        if self.check():
            if self.dist_to_target() == m:
                next_move.append(self.direction)
            elif self.dist_to_target() < m:
                next_move = [self.direction]

        if self.debug:
            print(next_move)

        self.direction = choice(next_move)
        self.set_align()

    def target(self):
        self.targetx = 0
        self.targety = 0

    def panic(self):
        # Pac-Man съел большую точку
        self.panic_time = clock()
        if self.attack:
            self.attack = False
            self.speed -= 1

            if settings.level == 1:
                settings.energizer_time = 6
            elif settings.level == 2:
                settings.energizer_time = 4
            elif settings.level == 3:
                settings.energizer_time = 2

            self.ghost_pic, self.scared_pic = self.scared_pic, self.ghost_pic

    def end_panic(self):
        if not self.attack:
            self.attack = True
            self.speed += 1

            self.ghost_pic, self.scared_pic = self.scared_pic, self.ghost_pic

    # смерть госта
    def kill(self):
        self.direction = 0
        self.set_pos(self.startx, self.starty)
        self.killed_time = clock()


class Blinky(Ghost):
    x, y = 0, 0

    def __init__(self, x, y):
        super().__init__(x, y, 'images/ghost_red.png')
        self.killed_time = clock() - 2
        self.direction = 1

    def target(self):
        self.targetx = Pacman.x
        self.targety = Pacman.y

        Blinky.x = self.ceilx
        Blinky.y = self.ceily

        if not self.attack:
            self.targetx = len(settings.walls_on_map) - self.targetx
            self.targety = len(settings.walls_on_map) - self.targety


class Pinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, 'images/ghost_pink.png')
        self.killed_time = clock() - 3

    def target(self):
        self.targetx = Pacman.x + Pacman.go[0] * 4
        self.targety = Pacman.y + Pacman.go[1] * 4

        if not self.attack:
            self.targetx = len(settings.walls_on_map) - self.targetx
            self.targety = len(settings.walls_on_map) - self.targety


class Inky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, 'images/ghost_blue.png')
        self.killed_time = clock() - 1

    def target(self):
        self.targetx = Pacman.x
        self.targety = Pacman.y

        self.targetx += (self.targetx - Blinky.x)
        self.targety += (self.targety - Blinky.y)

        if not self.attack:
            self.targetx = len(settings.walls_on_map) - self.targetx
            self.targety = len(settings.walls_on_map) - self.targety


class Clyde(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, 'images/ghost_yellow.png')

    def target(self):
        self.targetx = Pacman.x
        self.targety = Pacman.y

        if not self.attack:
            self.targetx = len(settings.walls_on_map) - self.targetx
            self.targety = len(settings.walls_on_map) - self.targety

        if self.dist_to_target() <= 8 ** 2:
            self.targetx = 0
            self.targety = len(settings.walls_on_map)
