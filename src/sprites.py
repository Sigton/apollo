import pygame


class Rocket(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("src/resources/rocket.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, display):
        display.blit(self.image, self.rect.topleft)


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


class Debris(pygame.sprite.Sprite):

    def __init__(self, x, y, speed=20):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("src/resources/debris.png").convert_alpha()
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed

    def update(self):

        self.rect.y += self.speed

    def draw(self, display):

        display.blit(self.image, self.rect.topleft)


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
