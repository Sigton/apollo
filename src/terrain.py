import pygame
import json
import os

from src import constants

"""
writes/loads terrain to the json files
"""


class LevelData:

    save_file = None
    load_dir = None

    tile_colours = [0, 255]

    def __init__(self, savefile, loadfile, level):

        self.save_file = savefile

        self.load_dir = os.listdir(loadfile)

        self.level_data = []

    def load_data(self):

        # loads from json file

        with open(self.save_file, 'r') as infile:
            data = json.load(infile)

        return data

    def write_data(self):

        for file in self.load_dir:

            pix_array = pygame.PixelArray(file)

            x = 0
            for column in pix_array:
                y = 0
                for pixel in column:

                    new_tile = []
                    tile_data = {}

                    new_tile.append((x, y))

                    if pixel in self.tile_colours:
                        n = 0
                        for color in self.tile_colours:
                            n += 1
                            if pixel == color:
                                tile_data['tile'] = n
                                tile_data['type'] = constants.TILE_TYPES[n]

                    else:
                        tile_data['tile'] = 0
                        tile_data['type'] = None

                    new_tile.append(tile_data)
                    self.level_data.append(new_tile)
                    y += 1
                x += 1

        with open(self.save_file, "w") as outfile:
            json.dump(self.level_data, outfile)

        return self.level_data
