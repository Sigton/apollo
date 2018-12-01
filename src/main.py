import pygame

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

        # game loop
        while not self.game_exit:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.game_exit = True


if __name__ == "__main__":

    game = Main()
    game.run()

    pygame.quit()
