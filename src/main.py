import pygame
from pygame.locals import *

from src import text


class Main:

    def __init__(self):

        pygame.init()

        self.display = pygame.display.set_mode((960, 720))

        self.clock = pygame.time.Clock()

        self.text_engine = text.TextEngine()

        self.writing = False
        self.current_writing = None
        self.to_write = ""
        self.writing_progress = 0

    def run(self):

        game_exit = False

        while not game_exit:

            for event in pygame.event.get():
                if event.type == QUIT:
                    game_exit = True

                if event.type == KEYDOWN:
                    pass

            if self.writing:
                pass
            else:
                self.write("Hello", 10, 10)

            # draw code
            self.display.fill((0, 0, 0))

            self.clock.tick(60)
            pygame.display.flip()

    def write(self, text, x, y):

        if self.current_writing is None:
            # create new writing
            pass
        elif self.writing_progress == len(self.to_write)-1:
            # end writing
            pass
        else:
            # write new letter
            pass


if __name__ == "__main__":
    game = Main()
    game.run()

    pygame.quit()
