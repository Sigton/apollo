import pygame
from pygame.locals import *

from src import constants
from src import player

"""
main.py

This is where the magic happens
"""


class Main:

    def __init__(self):

        # game initialisation
        pygame.mixer.pre_init(22050, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        self.display = pygame.display.set_mode(constants.DISPLAY_SIZE)

        pygame.display.set_caption("game name")

        self.clock = pygame.time.Clock()

        self.player = player.Player()

        self.level_list = []

        # populate level list

        self.current_level_num = 0
        self.current_level = self.level_list[self.current_level_num](self.player)

        self.player.level = self.current_level

        self.game_exit = False

    def run(self):

        run = 0
        jump = False

        # game loop
        while not self.game_exit:
            for event in pygame.event.get():

                if event.type == QUIT:
                    self.game_exit = True

                elif event.type == KEYDOWN:
                    if event.key in (K_LEFT, K_a):
                        run = -1
                    elif event.key in (K_RIGHT, K_d):
                        run = 1

                    if event.key in (K_SPACE, K_w, K_UP):
                        jump = True

                elif event.type == KEYUP:
                    if event.key in (K_LEFT, K_a) and not run == 1:
                        run = 0
                    elif event.key in (K_RIGHT, K_d) and not run == -1:
                        run = 0
                    elif event.key in (K_SPACE, K_w, K_UP):
                        jump = False

        obstacle_hits = pygame.sprite.spritecollide(player, self.current_level.obstalcles, False)
        if len(obstacle_hits):
            self.player.reset()

        # Updating
        self.player.update()
        self.current_level.update()

        # Drawing
        self.current_level.draw(self.display)
        self.player.draw(self.display)

        self.clock.tick(60)
        pygame.display.flip()


if __name__ == "__main__":

    game = Main()
    game.run()

    pygame.quit()
