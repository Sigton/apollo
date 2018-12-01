import pygame
from pygame.locals import *

import random

from src import text
from src import story
from src import sprites


class Main:

    def __init__(self):

        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.mixer.init()
        pygame.init()

        self.display = pygame.display.set_mode((960, 720))
        self.background = pygame.image.load("src/resources/background.png")
        self.flicker = pygame.image.load("src/resources/flicker.png")

        pygame.mixer.music.load("src/resources/music.mp3")
        self.key_sounds = [pygame.mixer.Sound("src/resources/keypress.wav"),
                           pygame.mixer.Sound("src/resources/keypress1.wav"),
                           pygame.mixer.Sound("src/resources/keypress2.wav"),
                           pygame.mixer.Sound("src/resources/keypress3.wav"),
                           pygame.mixer.Sound("src/resources/keypress4.wav")]
        [sound.set_volume(0.3) for sound in self.key_sounds]

        self.ambient_sound = pygame.mixer.Sound("src/resources/ambient.wav")
        self.rocket_sound = pygame.mixer.Sound("src/resources/rocket.wav")
        self.rocket_sound.set_volume(0.5)

        self.clock = pygame.time.Clock()

        self.rocket = sprites.Rocket(690, 255)
        self.flame = sprites.Flame(690, 455)

        self.text_engine = text.TextEngine()

        self.writing = False
        self.current_writing = None
        self.to_write = ""
        self.writing_progress = 0

        self.text_queue = []

        self.character_limit = 46

        self.story_engine = story.StoryEngine()

        self.story_next = False
        self.can_progress = True

        self.play_click = 0

    def run(self):

        pygame.mixer.music.play(-1)
        self.ambient_sound.play(-1)

        game_exit = False
        flicker_pos = 0
        write_delay = 0
        response = 0

        while not game_exit:

            for event in pygame.event.get():
                if event.type == QUIT:
                    game_exit = True

                if event.type == KEYDOWN:
                    if not self.can_progress:
                        if event.key == K_1:
                            self.can_progress = True
                            self.text_engine.get_text(": ")[-1].text_append("1")
                            response = 1
                        elif event.key == K_2:
                            self.can_progress = True
                            self.text_engine.get_text(": ")[-1].text_append("2")
                            response = 2
                        elif event.key == K_3:
                            self.can_progress = True
                            self.text_engine.get_text(": ")[-1].text_append("3")
                            response = 3

            if self.story_next and self.can_progress:
                if self.story_engine.progress == len(self.story_engine.story)-1:
                    self.story_engine.switch_story(self.story_engine.story[self.story_engine.progress][response-1])
                    response = 0

                self.add_to_queue(self.story_engine.story[self.story_engine.progress])
                self.story_engine.progress += 1
                self.story_next = False

                if self.story_engine.story[self.story_engine.progress - 1] == ": ":
                    self.can_progress = False

            if write_delay > 0:
                write_delay -= 1
            else:
                self.write()
                write_delay = 1

            flicker_pos = (flicker_pos + 1) % 16
            self.flame.update()

            # draw code
            self.display.blit(self.background, (0, 0))
            self.display.blit(self.flicker, (0, flicker_pos))
            self.text_engine.draw(self.display)

            self.rocket.draw(self.display)
            self.flame.draw(self.display)

            self.clock.tick(60)
            pygame.display.flip()

    def add_to_queue(self, new_text):

        if len(new_text) > self.character_limit:
            split_text = new_text.split(" ")
            n = len(split_text) - 1
            while len(" ".join(split_text[0:n])) > self.character_limit:
                n -= 1
            self.text_queue += [" ".join(split_text[0:n])]
            self.add_to_queue(" ".join(split_text[n:]))
        else:
            self.text_queue += [new_text]

    def write(self):

        if self.current_writing is None:
            # create new writing

            if not len(self.text_queue):
                if not self.story_next:
                    self.story_next = True
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
            if self.to_write[self.writing_progress] != " ":
                if self.play_click:
                    random.choice(self.key_sounds).play()
                self.play_click = 1 - self.play_click


if __name__ == "__main__":
    game = Main()
    game.run()

    pygame.quit()
