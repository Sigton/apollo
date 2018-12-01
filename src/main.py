import pygame

from src import constants

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
