"""
Class that makes an individual tile on the screen
"""

import pygame

from src import spritesheet

# list each platform with co-ords on spritesheet here


# tuple of all platforms
platforms = ()


class Platform(pygame.sprite.Sprite):

    def __init__(self, spritesheetdata, x, y, layer=0):

        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = sprite
