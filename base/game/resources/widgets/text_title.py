import pygame as pg
from .widget import Widget
from settings import SettingsLoader

config = SettingsLoader()

COLOR_BLANCO = config.get_key('COLOR_BLANCO')
COLOR_BLANCO = tuple(map(int, COLOR_BLANCO.strip('()').split(', ')))


class TextTitle(Widget):

    def __init__(self, x, y, texto, pantalla, font_size=50):
        super().__init__(x, y, texto, pantalla, font_size)
        # config.get_key('BUBBLE_GUMS, self.font_size)
        self.font = pg.font.Font(config.get_key(
            'BUBBLE_BOBBLE'), self.font_size)
        self.image = self.font.render(self.texto, True, COLOR_BLANCO)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        super().draw()

    def update(self):
        self.draw()
