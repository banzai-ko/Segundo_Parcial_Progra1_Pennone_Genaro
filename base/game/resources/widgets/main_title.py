import pygame as pg
from .widget import Widget
from settings import SettingsLoader

config = SettingsLoader()


class MainTitle(Widget):

    def __init__(self, x, y, texto, pantalla, font_size=50):
        super().__init__(x, y, texto, pantalla, font_size)
        self.font = pg.font.Font(config.get_key('BUBBLEBOY'), self.font_size)
        self.image = self.font.render(
            self.texto, True, config.get_key('COLOR_BLANCO'))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        super().draw()

    def update(self):
        self.draw()
