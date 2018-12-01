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
        self.flicker = pygame.image.load("src/resources/flicker.png")

        pygame.mixer.music.load("src/resources/music.mp3")
        self.key_sounds = [pygame.mixer.Sound("src/resources/keypress.wav"),
                           pygame.mixer.Sound("src/resources/keypress1.wav"),
                           pygame.mixer.Sound("src/resources/keypress2.wav"),
                           pygame.mixer.Sound("src/resources/keypress3.wav"),
                           pygame.mixer.Sound("src/resources/keypress4.wav")]
        [sound.set_volume(0.1) for sound in self.key_sounds]

        self.ambient_sound = pygame.mixer.Sound("src/resources/ambient.wav")
        self.rocket_sound = pygame.mixer.Sound("src/resources/rocket.wav")
        self.rocket_sound.set_volume(0.5)
        self.ambient_sound.set_volume(0.5)

        self.clock = pygame.time.Clock()

        self.rocket = sprites.Rocket(615, 550)
        self.obstacles = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.backgrounds = pygame.sprite.Group()
        self.backgrounds.add(sprites.Background(260, -720))
        self.backgrounds.add(sprites.Background(260, 0))

        self.text_engine = text.TextEngine()

        self.writing = False
        self.current_writing = None
        self.to_write = ""
        self.writing_progress = 0

        self.text_queue = []

        self.character_limit = 28

        self.play_click = 0

        self.obstacle_classes = [sprites.Debris, sprites.Meteor]

    def run(self):

        self.add_to_queue(">>> Apollo 18 System Info")
        self.add_to_queue("----------------------------")
        self.add_to_queue("> Velocity |-------#-------|")
        self.add_to_queue(">   Fuel   |###############|")
        self.add_to_queue(">  Damage  |---------------|")
        self.add_to_queue(">  Oxygen  |###############|")
        self.add_to_queue("----------------------------")
        self.add_to_queue(">>> Apollo 18 Mission Log")
        self.add_to_queue("----------------------------")

        pygame.mixer.music.play(-1)
        self.ambient_sound.play(-1)

        game_exit = False
        flicker_pos = 0
        moving = 0
        debris_delay = 360

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

            if self.text_engine.get_lines() > 6:
                self.text_engine.text_surfs[2].set_text("> Velocity |{}#{}|".format(
                    ('-'*(7-int(abs(self.rocket.xv)//2))) +
                    ('#'*int(abs(self.rocket.xv)//2))if self.rocket.xv < 0else'-'*7,
                    ('#'*int(self.rocket.xv//2))+('-'*int(7-(self.rocket.xv//2))) if self.rocket.xv > 0 else '-' * 7
                ))
                self.text_engine.text_surfs[3].set_text(">   Fuel   |{}|".format(
                    '#' * int(self.rocket.fuel * 0.15) + '-' * (15 - int(self.rocket.fuel * 0.15))))
                self.text_engine.text_surfs[4].set_text(">  Damage  |{}|".format(
                    '#'*int(self.rocket.damage*0.15)+'-'*(15-int(self.rocket.damage*0.15))))

            self.write()

            flicker_pos = (flicker_pos + 1) % 16

            if debris_delay > 0:
                debris_delay -= 1
            else:
                self.create_debris(random.randint(300, 935), -75)
                debris_delay = 120

            self.backgrounds.update()
            self.rocket.update()
            self.obstacles.update()
            self.explosions.update()
            sprite_hit = pygame.sprite.spritecollide(self.rocket, self.obstacles, True)
            for hit in sprite_hit:
                self.create_explosion(hit.rect.centerx, hit.rect.bottom)
                self.rocket.damage += hit.damage_factor

            # draw code
            self.display.fill((0, 0, 0))

            self.backgrounds.draw(self.display)
            self.rocket.draw(self.display)
            self.obstacles.draw(self.display)
            self.explosions.draw(self.display)

            self.display.blit(self.flicker, (0, -flicker_pos))
            self.text_engine.draw(self.display)

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

        self.obstacles.add(random.choice(self.obstacle_classes)(x, y, random.randint(10, 15)))

    def create_explosion(self, x, y):

        self.explosions.add(sprites.Explosion(x, y))


if __name__ == "__main__":
    game = Main()
    game.run()

    pygame.quit()
