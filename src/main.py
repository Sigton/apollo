import pygame
from pygame.locals import *


class Main:

    def __init__(self):

        pygame.init()

        self.display = pygame.display.set_mode((960, 720))

        self.clock = pygame.time.Clock()

    def run(self):

        game_exit = False

        while not game_exit:

            for event in pygame.event.get():
                if event.type == QUIT:
                    game_exit = True

                if event.type == KEYUP:
                    pass

            # update code

            # draw code
            self.display.fill((0, 0, 0))

            self.clock.tick(60)
            pygame.display.flip()


if __name__ == "__main__":
    game = Main()
    game.run()

    pygame.quit()
