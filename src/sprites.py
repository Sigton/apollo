import pygame
import random


class Rocket(pygame.sprite.Sprite):

    def __init__(self, master, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.master = master

        self.xv = 0

        self.startx = x

        self.image = pygame.image.load("src/resources/rocket.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.flame = Flame(x, y+100)

        self.mini_flame_left = Flame(x-10, y+45, False, True, False)
        self.mini_flame_right = Flame(x+20, y+45, False, True, True)

        self.show_mini = 0

        self.fuel = 100
        self.damage = 0
        self.oxygen = 100

        self.leaking_o2 = False

        self.max_speed = 14

    def update(self):
        self.flame.update()

        self.rect.x += self.xv

        if self.xv > self.max_speed:
            self.xv = self.max_speed
        if self.xv < -self.max_speed:
            self.xv = -self.max_speed

        self.fuel -= abs(self.xv)/170
        if self.leaking_o2:
            self.max_speed = 14-(0.07*self.damage)
            self.oxygen -= self.damage/1200

        if self.fuel < 0:
            self.fuel = 0
        if self.oxygen < 0:
            self.oxygen = 0
        if self.damage > 100:
            self.damage = 100

        self.flame.rect.topleft = (self.rect.x, self.rect.y+100)

        if self.show_mini > 0:
            self.mini_flame_right.update()
            self.mini_flame_right.rect.topleft = (self.rect.x + 20, self.rect.y + 45)
        elif self.show_mini < 0:
            self.mini_flame_left.update()
            self.mini_flame_left.rect.topleft = (self.rect.x - 10, self.rect.y + 45)

        if self.rect.right < 300:
            self.rect.left = 960
        if self.rect.left > 960:
            self.rect.right = 300

        if self.rect.top > 960:
            self.rect.bottom = -31
            self.reset()

    def move_left(self):

        self.xv -= .5

    def move_right(self):

        self.xv += .5

    def reset(self):
        self.rect.x = self.startx
        self.xv = 0
        self.fuel = 100
        self.damage = 0
        self.oxygen = 100
        self.leaking_o2 = False
        self.max_speed = 14
        self.master.reset()

    def draw(self, display):
        display.blit(self.image, self.rect.topleft)
        self.flame.draw(display)

        if self.show_mini > 0:
            self.mini_flame_right.draw(display)
        elif self.show_mini < 0:
            self.mini_flame_left.draw(display)


class Flame:

    def __init__(self, x, y, alien=False, mini=False, right=False):

        if alien:
            self.images = [
                pygame.image.load("src/resources/flame3.png"),
                pygame.image.load("src/resources/flame4.png")
            ]
        elif mini:
            if right:
                self.images = [
                    pygame.image.load("src/resources/miniflame3.png"),
                    pygame.image.load("src/resources/miniflame4.png")
                ]
            else:
                self.images = [
                    pygame.image.load("src/resources/miniflame1.png"),
                    pygame.image.load("src/resources/miniflame2.png")
                ]
        else:
            self.images = [
                pygame.image.load("src/resources/flame1.png"),
                pygame.image.load("src/resources/flame2.png")
            ]

        self.image = self.images[0]
        self.current_image = 0

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.timer = 6

    def update(self):

        if self.timer > 0:
            self.timer -= 1
        else:
            self.current_image = 1 - self.current_image
            self.image = self.images[self.current_image]
            self.timer = 6

    def draw(self, display):
        display.blit(self.image, self.rect.topleft)


class ObstacleBase(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.image = None
        self.rect = None
        self.speed = None
        self.damage_factor = None
        self.direction = 0

    def update(self):

        self.rect.y += self.speed
        self.rect.x += (self.speed * self.direction) / 2

        if self.rect.right < 300:
            self.rect.left = 960
        if self.rect.left > 960:
            self.rect.right = 300

        if self.rect.y >= 720:
            self.kill()

    def draw(self, display):

        display.blit(self.image, self.rect.topleft)


class Debris(ObstacleBase):

    def __init__(self, x, y, speed=10, diagonal=False, direction=0):

        ObstacleBase.__init__(self)

        if not diagonal:
            self.image = random.choice([pygame.image.load("src/resources/debris.png").convert_alpha(),
                                        pygame.image.load("src/resources/debris1.png").convert_alpha()])
        else:
            if direction > 0:
                self.image = pygame.image.load("src/resources/debris3.png").convert_alpha()
            else:
                self.image = pygame.image.load("src/resources/debris2.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed
        self.damage_factor = speed*0.7

        self.direction = direction


class Meteor(ObstacleBase):

    def __init__(self, x, y, speed=7, diagonal=False, direction=0):

        ObstacleBase.__init__(self)

        if not diagonal:
            self.image = random.choice([pygame.image.load("src/resources/meteor.png").convert_alpha(),
                                        pygame.image.load("src/resources/meteor1.png").convert_alpha()])
        else:
            if direction > 0:
                self.image = pygame.image.load("src/resources/meteor3.png").convert_alpha()
            else:
                self.image = pygame.image.load("src/resources/meteor2.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed
        self.damage_factor = speed

        self.direction = direction


class Alien(pygame.sprite.Sprite):

    def __init__(self, x, y, speed=1):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("src/resources/alien.png").convert_alpha()
        self.shoot_sound = pygame.mixer.Sound("src/resources/lasershoot.wav")

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.flame = Flame(x+30, y-20, True)

        self.speed = speed
        self.damage_factor = 10

        self.x_move = 120
        self.x_move_counter = self.x_move//2
        self.dir = 1

    def update(self):

        self.flame.update()

        self.rect.x += 2 * self.dir

        if self.rect.right < 300:
            self.rect.left = 960
        if self.rect.left > 960:
            self.rect.right = 300

        if self.x_move_counter > 0:
            self.x_move_counter -= 1
        else:
            self.x_move_counter = self.x_move
            self.dir = -self.dir

        if self.x_move_counter == self.x_move // 2:
            self.shoot()

        self.rect.y += self.speed

        self.flame.rect.topleft = (self.rect.x + 30, self.rect.y - 20)

        if self.flame.rect.y >= 720:
            self.kill()

    def shoot(self):
        self.groups()[0].add(Bullet(self.rect.centerx, self.rect.bottom))
        self.shoot_sound.play()

    def draw(self, display):

        display.blit(self.image, self.rect.topleft)
        self.flame.draw(display)


class Explosion(pygame.sprite.Sprite):

    def __init__(self, x, y, lifetime=21):

        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load("src/resources/explosion.png"),
                       pygame.image.load("src/resources/explosion1.png"),
                       pygame.image.load("src/resources/explosion2.png")]
        self.image = self.images[2]
        self.rect = self.image.get_rect()

        self.center = (x, y)
        self.rect.center = (x, y)

        self.lifetime = lifetime

    def update(self):

        self.lifetime -= 1

        if self.lifetime == 2:
            self.image = self.images[2]
            self.rect = self.image.get_rect()
        elif self.lifetime in [18, 4]:
            self.image = self.images[1]
            self.rect = self.image.get_rect()
        elif self.lifetime == 15:
            self.image = self.images[0]
            self.rect = self.image.get_rect()
        self.rect.center = self.center

        if self.lifetime <= 0:
            self.kill()

    def draw(self, display):

        display.blit(self.image, self.rect.topleft)


class Background(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("src/resources/background.png")
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):

        self.rect.y += 1

        if self.rect.top >= 720:
            self.rect.bottom = 0

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))


class Bullet(ObstacleBase):

    def __init__(self, x, y, speed=15):

        ObstacleBase.__init__(self)

        self.image = pygame.image.load("src/resources/bullet.png")

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed
        self.damage_factor = speed


class WarningManager:

    def __init__(self):

        self.warnings = pygame.sprite.Group()

        self.flash = 60

        self.beep = pygame.mixer.Sound("src/resources/beep2.wav")
        self.beep.set_volume(0.5)
        self.alarm = pygame.mixer.Sound("src/resources/alarm.wav")
        self.alarm.set_volume(0.5)

    def update(self):

        if self.flash > 0:
            self.flash -= 1
        else:
            if len(self.warnings):
                self.beep.play()
            self.flash = 60

    def add(self, warning_type):

        if self.has_warning(warning_type):
            return

        self.alarm.play()
        new_warning = WarningMessage(warning_type)
        self.warnings.add(new_warning)
        new_warning.rect.centerx = 630
        new_warning.rect.y = 200 + len(self.warnings)*40

    def has_warning(self, warning_type):

        return True if warning_type in [x.type for x in self.warnings] else False

    def remove(self, warning_type):

        pass

    def clear(self):

        self.warnings.empty()

    def draw(self, display):

        if self.flash >= 30:
            [warning.draw(display) for warning in self.warnings]


class WarningMessage(pygame.sprite.Sprite):

    def __init__(self, warning_type):

        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load("src/resources/oxygenwarning.png"),
                       pygame.image.load("src/resources/damagewarning.png"),
                       pygame.image.load("src/resources/fuelwarning.png")]
        self.image = self.images[warning_type]

        self.rect = self.image.get_rect()

        self.type = warning_type

        self.flash = 60

    def draw(self, display):

        display.blit(self.image, self.rect.topleft)


class GameEndSign(pygame.sprite.Sprite):

    def __init__(self, end_type):

        pygame.sprite.Sprite.__init__(self)

        self.images = [
            pygame.image.load("src/resources/missionfailed.png"),
            pygame.image.load("src/resources/outofoxygen.png"),
            pygame.image.load("src/resources/shipdestroyed.png"),
            pygame.image.load("src/resources/outoffuel.png")
        ]

        self.image1 = self.images[0]
        self.image2 = self.images[end_type]

        self.rect1 = self.image1.get_rect()
        self.rect1.centerx = 630
        self.rect1.y = 200

        self.rect2 = self.image2.get_rect()
        self.rect2.centerx = 630
        self.rect2.y = 240

        self.type = end_type

    def draw(self, display):

        display.blit(self.image1, self.rect1.topleft)
        display.blit(self.image2, self.rect2.topleft)
