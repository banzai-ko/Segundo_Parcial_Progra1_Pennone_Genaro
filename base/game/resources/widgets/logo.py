import pygame as pg
from .widget import Widget
from settings import SCREEN as DIMENSION_PANTALLA, THISORTHAT


class Logo(Widget):

    def __init__(self, x, y, texto, pantalla, font_size = 50):
        super().__init__(x, y, texto, pantalla, font_size)
        self.logo = pg.image.load(THISORTHAT).convert_alpha()
        logo_x = DIMENSION_PANTALLA[0] // 2 - self.logo.get_width() // 2  # Center horizontally
        logo_y = DIMENSION_PANTALLA[1] // 2 - 400  # Place above the main title
        self.rect = self.logo.get_rect()
        self.rect.x = logo_x
        self.rect.y = logo_y
        self.image = self.logo
    def draw(self):
        super().draw()
    
    def update(self):
        self.draw()