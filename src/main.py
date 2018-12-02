import pygame
from pygame.locals import *

import random
import json

from src import text
from src import sprites


class Main:

    def __init__(self):

        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.mixer.init()
        pygame.init()

        pygame.mixer.set_num_channels(16)

        self.display = pygame.display.set_mode((960, 720))
        pygame.display.set_caption("Apollo")

        icon = pygame.image.load("src/resources/icon.png")
        pygame.display.set_icon(icon)

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
        self.ambient_sound.set_volume(0.3)

        self.small_explosion_sound = pygame.mixer.Sound("src/resources/explosion.wav")
        self.small_explosion_sound.set_volume(0.4)
        self.beep_sound = pygame.mixer.Sound("src/resources/beep.wav")
        self.beep_sound.set_volume(0.5)
        self.big_explosion_sound = pygame.mixer.Sound("src/resources/explosion2.wav")
        self.big_explosion_sound.set_volume(0.5)
        self.whoosh = pygame.mixer.Sound("src/resources/whoosh.wav")
        self.whoosh.set_volume(0.6)
        self.whoosh2 = pygame.mixer.Sound("src/resources/whoosh2.wav")
        self.whoosh2.set_volume(0.3)
        self.blip = pygame.mixer.Sound("src/resources/blip.wav")
        self.blip.set_volume(0.5)

        self.clock = pygame.time.Clock()

        self.rocket = sprites.Rocket(self, 615, -106)
        self.obstacles = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.backgrounds = pygame.sprite.Group()
        self.misc = pygame.sprite.Group()
        self.backgrounds.add(sprites.Background(260, -720))
        self.backgrounds.add(sprites.Background(260, 0))

        self.warning_manager = sprites.WarningManager()

        self.text_engine = text.TextEngine()

        self.writing = False
        self.current_writing = None
        self.to_write = ""
        self.writing_progress = 0

        self.text_queue = []

        self.character_limit = 28

        self.play_click = 0

        self.obstacle_selection_prob = [0, 0, 0, 1, 1]
        self.obstacle_classes = [sprites.Debris, sprites.Meteor, sprites.Alien]

        self.score = 0

        with open("src/highscore.json", 'r') as infile:
            self.highscore = json.load(infile)["highscore"]

        self.speed_ranges = [range(10, 15),
                             range(7, 12),
                             [2, 2]]

        self.initial_obstacle_prob = self.obstacle_selection_prob
        self.initial_speed = self.speed_ranges

        self.rocket_move_vertical_counter = 328

        self.fuel_threshold = 90
        self.oxygen_threshold = 90
        self.score_threshold = 10000

        self.resetting = False

        self.can_spawn = False

    def run(self):

        str_score = str(self.highscore)
        while len(str(str_score)) < 15:
            str_score = "0" + str_score

        self.add_to_queue(">>> Apollo 18 System Info")
        self.add_to_queue("----------------------------")
        self.add_to_queue("> Velocity |-------#-------|")
        self.add_to_queue(">   Fuel   |###############|")
        self.add_to_queue(">  Damage  |---------------|")
        self.add_to_queue(">  Oxygen  |###############|")
        self.add_to_queue(">   Score  |000000000000000|")
        self.add_to_queue("> Highscore|{}|".format(str_score))
        self.add_to_queue("----------------------------")
        self.add_to_queue(">>> Apollo 18 Mission Log")
        self.add_to_queue("----------------------------")
        self.add_to_queue(">>> Move to begin.")
        self.add_to_queue(">>> <Enter> for controls.")

        pygame.mixer.music.play(-1)
        self.ambient_sound.play(-1)

        game_exit = False
        flicker_pos = 0
        moving = 0
        debris_delay = 120
        spawn_intervals = 120
        diff_interval = 3

        while not game_exit:

            for event in pygame.event.get():
                if event.type == QUIT:
                    game_exit = True

                if event.type == KEYDOWN:

                    if self.rocket_move_vertical_counter == 0:
                        if not self.can_spawn:
                            if event.key in (K_LEFT, K_a, K_RIGHT, K_d):
                                self.can_spawn = True
                                self.add_to_queue(">>> Mission started.")
                                self.beep_sound.play()
                            elif event.key == K_RETURN:
                                self.add_to_queue(">>> A/D or LEFT/RIGHT to move.")
                                self.add_to_queue(">>> Dodge obstacles but conserve fuel.")
                                self.add_to_queue(">>> Good luck. Mission started.")
                                self.can_spawn = True
                                self.beep_sound.play()

                        elif event.key in (K_LEFT, K_a):
                            moving = -1
                            self.rocket.show_mini = 1
                            self.whoosh.play()
                        elif event.key in (K_RIGHT, K_d):
                            moving = 1
                            self.rocket.show_mini = -1
                            self.whoosh.play()

                if event.type == KEYUP:
                    if event.key in (K_LEFT, K_a) and not moving == 1:
                        moving = 0
                        self.rocket.show_mini = 0
                    elif event.key in (K_RIGHT, K_d) and not moving == -1:
                        moving = 0
                        self.rocket.show_mini = 0
            if self.rocket_move_vertical_counter > 0:
                self.rocket.rect.y += 2
                self.rocket_move_vertical_counter -= 1
            elif self.resetting:
                self.add_to_queue(">>> Move to begin.")
                self.add_to_queue(">>> <Enter> for controls.")
                self.resetting = False

            if (self.rocket.damage >= 100 or self.rocket.fuel <= 0 or self.rocket.oxygen <= 0) and self.can_spawn:
                self.rocket_move_vertical_counter = 548
                self.can_spawn = False
                self.warning_manager.clear()
                if self.rocket.fuel <= 0:
                    end_type = 3
                elif self.rocket.oxygen <= 0:
                    end_type = 1
                else:
                    end_type = 2
                    self.explosion_spread()

                self.misc.add(sprites.GameEndSign(end_type))
            else:
                if self.can_spawn:
                    if moving == -1:
                        self.rocket.move_left()
                    if moving == 1:
                        self.rocket.move_right()

            self.update_hud()

            flicker_pos = (flicker_pos + 1) % 16

            if self.can_spawn:
                self.score += 89
                if debris_delay > 0:
                    debris_delay -= 1
                else:
                    self.create_debris(random.randint(300, 935), -75)
                    debris_delay = spawn_intervals
                    diff_interval -= 1
                    if diff_interval == 0:
                        if spawn_intervals > 10:
                            spawn_intervals -= 3
                        self.obstacle_selection_prob += [random.randint(0, 2)]
                        s = random.randint(0, 1)
                        self.speed_ranges[s] = range(self.speed_ranges[s][0]+1, self.speed_ranges[s][-1]+2)
                        diff_interval = 3

            self.backgrounds.update()
            self.rocket.update()
            self.obstacles.update()
            self.explosions.update()
            sprite_hit = pygame.sprite.spritecollide(self.rocket, self.obstacles, False)
            for hit in sprite_hit:

                if self.rocket.rect.bottom < hit.rect.bottom:
                    continue

                hit.kill()
                self.create_explosion(hit.rect.centerx, hit.rect.bottom)
                self.rocket.damage += hit.damage_factor
                self.add_to_queue(">>> {} damage taken.".format(int(hit.damage_factor)))
                if not self.rocket.leaking_o2:
                    self.rocket.leaking_o2 = True
                self.small_explosion_sound.play()

            self.warning_manager.update()
            self.misc.update()

            # draw code
            self.display.fill((0, 0, 0))

            self.backgrounds.draw(self.display)
            self.rocket.draw(self.display)
            for obstacle in self.obstacles:
                obstacle.draw(self.display)
            self.explosions.draw(self.display)
            self.warning_manager.draw(self.display)
            [x.draw(self.display) for x in self.misc]

            self.display.blit(self.flicker, (0, -flicker_pos))
            self.text_engine.draw(self.display)

            self.clock.tick(60)
            pygame.display.flip()

        with open("src/highscore.json", 'w') as outfile:
            json.dump({"highscore": self.highscore}, outfile)

    def update_hud(self):

        if self.text_engine.get_lines() > 8:
            self.text_engine.text_surfs[2].set_text("> Velocity |{}#{}|".format(
                ('-' * (7 - int(abs(self.rocket.xv) // 2))) +
                ('#' * int(abs(self.rocket.xv) // 2)) if self.rocket.xv < 0 else '-' * 7,
                ('#' * int(self.rocket.xv // 2)) + (
                        '-' * int(7 - (self.rocket.xv // 2))) if self.rocket.xv > 0 else '-' * 7
            ))
            self.text_engine.text_surfs[3].set_text(">   Fuel   |{}|".format(
                '#' * int(self.rocket.fuel * 0.15) + '-' * (15 - int(self.rocket.fuel * 0.15))))
            self.text_engine.text_surfs[4].set_text(">  Damage  |{}|".format(
                '#' * int(self.rocket.damage * 0.15) + '-' * (15 - int(self.rocket.damage * 0.15))))
            self.text_engine.text_surfs[5].set_text(">  Oxygen  |{}|".format(
                '#' * int(self.rocket.oxygen * 0.15) + '-' * (15 - int(self.rocket.oxygen* 0.15))))

            str_score = str(self.score)
            while len(str(str_score)) < 15:
                str_score = "0" + str_score
            self.text_engine.text_surfs[6].set_text(">   Score  |{}|".format(str_score))

            if self.score > self.score_threshold:
                self.blip.play()
                self.score_threshold += 10000

            if self.score > self.highscore:
                self.highscore = self.score
                self.text_engine.text_surfs[7].set_text("> Highscore|{}|".format(str_score))

        if self.rocket.fuel < self.fuel_threshold:
            self.add_to_queue(">>> Fuel at {}%.".format(self.fuel_threshold))
            self.fuel_threshold -= 10
            if self.fuel_threshold < 20 and self.can_spawn:
                self.warning_manager.add(2)

        if self.rocket.oxygen < self.oxygen_threshold:
            self.add_to_queue(">>> Oxygen at {}%.".format(self.oxygen_threshold))
            self.oxygen_threshold -= 10
            if self.oxygen_threshold < 20 and self.can_spawn:
                self.warning_manager.add(0)

        if self.rocket.damage >= 70 and self.can_spawn:
            self.warning_manager.add(1)

        self.write()

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

        sprite = random.choice(self.obstacle_selection_prob)
        self.obstacles.add(self.obstacle_classes[sprite](x, y, random.choice(self.speed_ranges[sprite])))
        self.whoosh2.play()

    def create_explosion(self, x, y):

        self.explosions.add(sprites.Explosion(x, y))

    def explosion_spread(self):

        self.create_explosion(self.rocket.rect.x, self.rocket.rect.y)
        self.create_explosion(self.rocket.rect.x+25, self.rocket.rect.y+30)
        self.create_explosion(self.rocket.rect.x+10, self.rocket.rect.y+50)
        self.create_explosion(self.rocket.rect.x+30, self.rocket.rect.y+80)
        self.create_explosion(self.rocket.rect.x-5, self.rocket.rect.y+110)
        self.big_explosion_sound.play()

    def reset(self):

        self.text_engine.clear()
        self.add_to_queue(">>> You scored: {}.".format(self.score))

        self.score = 0
        self.resetting = True

        self.misc.empty()

        self.speed_ranges = self.initial_speed
        self.obstacle_selection_prob = self.initial_obstacle_prob


if __name__ == "__main__":
    game = Main()
    game.run()

    pygame.quit()
