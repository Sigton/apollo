import pygame
from pygame.locals import *

from src import text


class Main:

    def __init__(self):

        pygame.init()

        self.display = pygame.display.set_mode((960, 720))
        self.background = pygame.image.load("src/resources/background.png")

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

            self.write("Hello and welcome to my amazing text-based game", 10, 10)

            # draw code
            self.display.blit(self.background, (0, 0))
            self.text_engine.draw(self.display)

            self.clock.tick(60)
            pygame.display.flip()

    def write(self, new_text, x, y):

        if self.current_writing is None:
            # create new writing
            self.writing = True
            self.to_write = new_text
            self.current_writing = text.Text(self.to_write[0], x, y)
            self.writing_progress = 0

            self.text_engine.add_text(self.current_writing)

        elif self.writing_progress == len(self.to_write)-1:
            # end writing
            self.writing = False
            self.to_write = ""
            self.current_writing = None
        else:
            # write new letter
            self.writing_progress += 1
            self.current_writing.text_append(self.to_write[self.writing_progress])


if __name__ == "__main__":
    game = Main()
    game.run()

    pygame.quit()
