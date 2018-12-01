import pygame
import json
import os

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
