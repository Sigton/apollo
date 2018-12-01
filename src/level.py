"""
contains the level classes
"""

import pygame

from src import constants
from src import tile


class Level:

    # level parent class
    # I'll make a child class of this for each level

    player = None  # ref to player

    def __init__(self, player):

        # solid things
        self.platforms = pygame.sprite.Group()

        self.player = player

        # number of layers of tiles in the level: this should hopefully stay small
        self.layer_range = 0

        self.background = pygame.image.load("src/resources/sprites/background.png")

    def update(self):

        # platforms don't interact with player, no need to update them
        pass

    def draw(self, display):

        display.fill(constants.BLACK)
        display.blit(self.background)

        for platform in self.platforms:
            platform.draw(display)

    def create_platform(self, tile_num, x, y, layer):

        platform = tile.Platform(tile_num, x, y, layer)
        self.platforms.add(platform)

    def create_level(self, data):

        pass
