import pygame as pg
from .widget import Widget
from settings import SettingsLoader

config = SettingsLoader()


class Logo(Widget):

    def __init__(self, x, y, texto, pantalla, font_size=0, key='THISORTHAT', size=""):
        super().__init__(x, y, texto, pantalla, font_size)
        self.logo = pg.image.load(config.get_key(key)).convert_alpha()
        if size != "":
            self.logo = pg.transform.scale(self.logo, size)
        self.rect = self.logo.get_rect()
        logo_width, logo_height = self.rect.size
        self.rect.x = x - logo_width // 2
        self.rect.y = y - logo_height // 2
        self.image = self.logo

    def draw(self):
        super().draw()

    def update(self):
        self.draw()
