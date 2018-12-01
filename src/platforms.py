"""
Class that makes an individual tile on the screen
"""

import pygame

from src import spritesheet

# list each platform with co-ords on spritesheet here
GROUND = (0, 0, 32, 32)
SPIKE = (32, 0, 32, 32)

# tuple of all platforms
platforms = (GROUND, SPIKE)


class Platform(pygame.sprite.Sprite):

    def __init__(self, spritesheetdata, x, y, layer=0):

        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = spritesheet.SpriteSheet("src/resources/terrain.png")

        self.image = sprite_sheet.get_image(spritesheetdata[0],
                                            spritesheetdata[1],
                                            spritesheetdata[2],
                                            spritesheetdata[3])

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.layer = layer

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
