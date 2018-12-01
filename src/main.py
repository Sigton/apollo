import pygame
from pygame.locals import *

import random

from src import text
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
        self.ambient_sound.set_volume(0.5)

        self.clock = pygame.time.Clock()

        self.rocket = sprites.Rocket(690, 255)
        self.debris = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self.text_engine = text.TextEngine()

        self.writing = False
        self.current_writing = None
        self.to_write = ""
        self.writing_progress = 0

        self.text_queue = []

        self.character_limit = 28

        self.play_click = 0

    def run(self):

        self.add_to_queue(">>> Apollo 18 System Info")

        pygame.mixer.music.play(-1)
        self.ambient_sound.play(-1)

        game_exit = False
        flicker_pos = 0
        write_delay = 0
        moving = 0

        while not game_exit:

            for event in pygame.event.get():
                if event.type == QUIT:
                    game_exit = True

                if event.type == KEYDOWN:
                    if event.key in (K_LEFT, K_a):
                        moving = -1
                    elif event.key in (K_RIGHT, K_d):
                        moving = 1

                if event.type == KEYUP:
                    if event.key in (K_LEFT, K_a) and not moving == 1:
                        moving = 0
                    elif event.key in (K_RIGHT, K_d) and not moving == -1:
                        moving = 0

            if moving == -1:
                self.rocket.move_left()
            if moving == 1:
                self.rocket.move_right()

            if write_delay > 0:
                write_delay -= 1
            else:
                self.write()
                write_delay = 1

            flicker_pos = (flicker_pos + 1) % 16

            self.rocket.update()
            self.debris.update()
            self.explosions.update()
            sprite_hit = pygame.sprite.spritecollide(self.rocket, self.debris, True)
            for hit in sprite_hit:
                self.create_explosion(hit.rect.centerx, hit.rect.bottom)

            # draw code
            self.display.fill((0, 0, 0))
            self.display.blit(self.background, (0, 0))
            self.display.blit(self.flicker, (0, flicker_pos))
            self.text_engine.draw(self.display)

            self.rocket.draw(self.display)
            self.debris.draw(self.display)
            self.explosions.draw(self.display)

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

    def create_debris(self, x, y):

        self.debris.add(sprites.Debris(x, y))

    def create_explosion(self, x, y):

        self.explosions.add(sprites.Explosion(x, y))


if __name__ == "__main__":
    game = Main()
    game.run()

    pygame.quit()
