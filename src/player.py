import pygame

from src import constants
from src import spritesheet

"""
defining the player class; platforming engine etc
"""


class Player(pygame.sprite.Sprite):

    # will contain a level class that we use to check for collision
    level = None

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.xv = 0
        self.yv = 0

        self.gravity = constants.PLAYER_GRAVITY
        self.friction = constants.PLAYER_FRICTION
        self.speed = constants.PLAYER_SPEED
        self.jump_height = constants.PLAYER_JUMP_HEIGHT

        sprite_sheet = spritesheet.SpriteSheet("src/resources/sprites/player.png")

        self.image = sprite_sheet.get_image(0, 0, 32, 64)

        self.rect = self.image.get_rect()

    def update(self):

        self.yv += self.gravity

        # temporary collision with bottom of screen: will remove once tiles are made
        if self.rect.y >= constants.DISPLAY_HEIGHT - self.rect.height and self.yv >= 0:
            self.yv = 0
            self.rect.y = constants.DISPLAY_HEIGHT - self.rect.height

        self.xv *= self.friction

        if abs(self.xv) <= 0.1:  # this will make animating look a little nicer later
            self.xv = 0

        self.rect.x += self.xv

        # collision detection time
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)


