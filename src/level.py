"""
contains the level classes
"""

import pygame

from src import constants
from src import platforms
from src import terrain


class Level:

    # level parent class
    # I'll make a child class of this for each level

    player = None  # ref to player

    def __init__(self, player):

        # solid things
        self.platforms = pygame.sprite.Group()
        # deadly things
        self.obstacles = pygame.sprite.Group()

        self.player = player

        # number of layers of tiles in the level: this should hopefully stay small
        self.layer_range = 0

        self.background = pygame.image.load("src/resources/sprites/background.png")

    def update(self):

        # platforms don't interact with player, no need to update them
        pass

    def draw(self, display):

        display.fill(constants.BLACK)
        display.blit(self.background, (0, 0))

        for platform in self.platforms:
            platform.draw(display)
        for obstacle in self.obstacles:
            obstacle.draw(display)

    def create_platform(self, tile_num, x, y, layer):

        platform = platforms.Platform(tile_num, x, y, layer)
        self.platforms.add(platform)

    def create_obstacle(self, tile_num, x, y, layer):

        platform = platforms.Platform(tile_num, x, y, layer)
        self.obstacles.add(platform)

    def create_level(self, data):

        layer = 0
        n = 0
        for tile in data:
            position = tile[0]
            tile_data = tile[1]

            if tile_data['type'] == "S":
                self.create_platform(platforms.platforms[tile_data['tile']], position[0]*32, position[1]*32, layer)
            elif tile_data['type'] == "O":
                self.create_obstacle(platforms.platforms[tile_data['tile']], position[0] * 32, position[1] * 32, layer)

            n += 1
            if n % 690 == 0:
                layer += 1


class Level01(Level):

    def __init__(self, player, write_data=True):

        Level.__init__(self, player)

        save_file = "src/leveldata/level1.json"
        tile_dir = "src/leveldata/level1"

        self.layer_range = 1

        level = terrain.LevelData(save_file, tile_dir)
        if write_data:
            level_data = level.write_data()
        else:
            level_data = level.load_data()

        self.create_level(level_data)
