import pygame


class Rocket(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.xv = 0

        self.image = pygame.image.load("src/resources/rocket.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.flame = Flame(x, y+100)

        self.fuel = 100
        self.damage = 0
        self.oxygen = 100

    def update(self):
        self.flame.update()

        self.rect.x += self.xv

        if self.xv > 14:
            self.xv = 14
        if self.xv < -14:
            self.xv = -14

        self.flame.rect.x = self.rect.x

        if self.rect.right < 300:
            self.rect.left = 960
        if self.rect.left > 960:
            self.rect.right = 300

    def move_left(self):

        self.xv -= .5

    def move_right(self):

        self.xv += .5

    def draw(self, display):
        display.blit(self.image, self.rect.topleft)
        self.flame.draw(display)


class Flame:

    def __init__(self, x, y):

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
