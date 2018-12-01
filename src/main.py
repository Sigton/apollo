import pygame
from pygame.locals import *

from src import text


class Main:

    def __init__(self):

        pygame.init()

        self.display = pygame.display.set_mode((960, 720))
        self.background = pygame.image.load("src/resources/background.png")
        self.flicker = pygame.image.load("src/resources/flicker.png")

        self.clock = pygame.time.Clock()

        self.text_engine = text.TextEngine()

        self.writing = False
        self.current_writing = None
        self.to_write = ""
        self.writing_progress = 0

        self.text_queue = []

        self.character_limit = 46

    def run(self):

        game_exit = False
        flicker_pos = 0

        self.add_to_queue("Hello and welcome to my amazing text-based game.")
        self.add_to_queue("""This will soon have far, far more content and I hope you look forward to seeing it all
slowly appear; I know I sure do!""".replace("\n", " "))

        while not game_exit:

            for event in pygame.event.get():
                if event.type == QUIT:
                    game_exit = True

                if event.type == KEYDOWN:
                    pass

            self.write()

            flicker_pos = (flicker_pos + 1) % 16

            # draw code
            self.display.blit(self.background, (0, 0))
            self.display.blit(self.flicker, (0, flicker_pos))
            self.text_engine.draw(self.display)

            self.clock.tick(60)
            pygame.display.flip()

    def add_to_queue(self, new_text):

        if len(new_text) > self.character_limit:
            split_text = new_text.split(" ")
            n = len(split_text) - 1
            while len(" ".join(split_text[0:n])) > self.character_limit:
                n -= 1
            self.text_queue += [[" ".join(split_text[0:n])]]
            self.add_to_queue(" ".join(split_text[n:]))
        else:
            self.text_queue += [[new_text]]

    def write(self):

        if self.current_writing is None:
            # create new writing

            if not len(self.text_queue):
                return

            new_text = self.text_queue.pop(0)

            self.writing = True
            self.to_write = new_text
            self.current_writing = text.Text(self.to_write[0], 10, ((self.text_engine.get_lines())*18)+4)
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
