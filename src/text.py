import pygame

FONT = None
WHITE = (255, 255, 255)


class TextEngine:

    def __init__(self):

        self.text_surfs = []

        global FONT
        FONT = pygame.font.SysFont("Courier", 18)

    def create_text(self, text, x, y, center=False):
        self.text_surfs.append(Text(text, x, y, center))

    def add_text(self, text_object):
        self.text_surfs.append(text_object)

    def get_text(self, content):
        for text in self.text_surfs:
            if text.text == content:
                return text
        return None

    def draw(self, display):

        for surf in self.text_surfs:
            surf.draw(display)


class Text:

    def __init__(self, text, x, y, center=False):

        self.text = text

        self.image = FONT.render(text, False, WHITE)
        self.rect = self.image.get_rect()
        if center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)

    def set_text(self, text, center=False):

        self.text = text

        old_pos = self.rect.center if center else self.rect.topleft
        self.image = FONT.render(text, False, WHITE)
        self.rect = self.image.get_rect()
        if center:
            self.rect.center = old_pos
        else:
            self.rect.topleft = old_pos

    def text_append(self, text, center=False):
        self.set_text(self.text + text, center)

    def set_pos(self, x, y, center=False):

        if center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)

    def draw(self, display):

        display.blit(self.image, self.rect.topleft)

