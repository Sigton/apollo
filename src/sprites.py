import pygame


class Rocket(pygame.sprite.Sprite):

    def __init__(self, master, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.master = master

        self.xv = 0

        self.startx = x

        self.image = pygame.image.load("src/resources/rocket.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.flame = Flame(x, y+100)

        self.fuel = 100
        self.damage = 0
        self.oxygen = 100

        self.leaking_o2 = False

        self.max_speed = 14

    def update(self):
        self.flame.update()

        self.rect.x += self.xv

        if self.xv > self.max_speed:
            self.xv = self.max_speed
        if self.xv < -self.max_speed:
            self.xv = -self.max_speed

        self.fuel -= abs(self.xv)/200
        if self.leaking_o2:
            self.max_speed = 14-(0.07*self.damage)
            self.oxygen -= self.damage/1000

        if self.fuel < 0:
            self.fuel = 0
        if self.oxygen < 0:
            self.oxygen = 0
        if self.damage > 100:
            self.damage = 100

        self.flame.rect.topleft = (self.rect.x, self.rect.y+100)

        if self.rect.right < 300:
            self.rect.left = 960
        if self.rect.left > 960:
            self.rect.right = 300

        if self.rect.top > 720:
            self.rect.bottom = -30
            self.reset()

    def move_left(self):

        self.xv -= .5

    def move_right(self):

        self.xv += .5

    def reset(self):
        self.rect.x = self.startx
        self.xv = 0
        self.fuel = 100
        self.damage = 0
        self.oxygen = 100
        self.leaking_o2 = False
        self.max_speed = 14
        self.master.reset()

    def draw(self, display):
        display.blit(self.image, self.rect.topleft)
        self.flame.draw(display)


class Flame:

    def __init__(self, x, y, alien=False, mini=False, right=False):

        if alien:
            self.images = [
                pygame.image.load("src/resources/flame3.png"),
                pygame.image.load("src/resources/flame4.png")
            ]
        elif mini:
            if right:
                self.images = [
                    pygame.image.load("src/resources/miniflame3.png"),
                    pygame.image.load("src/resources/miniflame4.png")
                ]
            else:
                self.images = [
                    pygame.image.load("src/resources/miniflame1.png"),
                    pygame.image.load("src/resources/miniflame2.png")
                ]
        else:
            self.images = [
                pygame.image.load("src/resources/flame1.png"),
                pygame.image.load("src/resources/flame2.png")
            ]

        self.image = self.images[0]
        self.current_image = 0

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.timer = 6

    def update(self):

        if self.timer > 0:
            self.timer -= 1
        else:
            self.current_image = 1 - self.current_image
            self.image = self.images[self.current_image]
            self.timer = 6

    def draw(self, display):
        display.blit(self.image, self.rect.topleft)


class ObstacleBase(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.image = None
        self.rect = None
        self.speed = None
        self.damage_factor = None

    def update(self):

        self.rect.y += self.speed
        if self.rect.y >= 720:
            self.kill()

    def draw(self, display):

        display.blit(self.image, self.rect.topleft)


class Debris(ObstacleBase):

    def __init__(self, x, y, speed=10):

        ObstacleBase.__init__(self)

        self.image = pygame.image.load("src/resources/debris.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed
        self.damage_factor = speed*0.7


class Meteor(ObstacleBase):

    def __init__(self, x, y, speed=7):

        ObstacleBase.__init__(self)

        self.image = pygame.image.load("src/resources/meteor.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed
        self.damage_factor = speed


class Alien(pygame.sprite.Sprite):

    def __init__(self, x, y, speed=1):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("src/resources/alien.png").convert_alpha()
        self.shoot_sound = pygame.mixer.Sound("src/resources/lasershoot.wav")

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.flame = Flame(x+30, y-20, True)

        self.speed = speed
        self.damage_factor = 10

        self.x_move = 120
        self.x_move_counter = self.x_move//2
        self.dir = 1

    def update(self):

        self.flame.update()

        self.rect.x += 2 * self.dir

        if self.rect.right < 300:
            self.rect.left = 960
        if self.rect.left > 960:
            self.rect.right = 300

        if self.x_move_counter > 0:
            self.x_move_counter -= 1
        else:
            self.x_move_counter = self.x_move
            self.dir = -self.dir

        if self.x_move_counter == self.x_move // 2:
            self.shoot()

        self.rect.y += self.speed

        self.flame.rect.topleft = (self.rect.x + 30, self.rect.y - 20)

        if self.rect.y >= 720:
            self.kill()

    def shoot(self):
        self.groups()[0].add(Bullet(self.rect.centerx, self.rect.bottom))
        self.shoot_sound.play()

    def draw(self, display):

        display.blit(self.image, self.rect.topleft)
        self.flame.draw(display)


class Explosion(pygame.sprite.Sprite):

    def __init__(self, x, y, lifetime=15):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("src/resources/explosion.png")
        self.rect = self.image.get_rect()

        self.rect.center = (x, y)

        self.lifetime = lifetime

    def update(self):

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

    def draw(self, display):

        display.blit(self.image, self.rect.topleft)


class Background(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("src/resources/background.png")
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):

        self.rect.y += 1

        if self.rect.top >= 720:
            self.rect.bottom = 0

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))


class Bullet(ObstacleBase):

    def __init__(self, x, y, speed=15):

        ObstacleBase.__init__(self)

        self.image = pygame.image.load("src/resources/bullet.png")

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed
        self.damage_factor = speed
