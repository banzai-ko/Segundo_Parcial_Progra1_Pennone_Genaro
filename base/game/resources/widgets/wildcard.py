import pygame as pg
from settings import SettingsLoader
from .button import Button  # Assuming Button is in a separate module

config = SettingsLoader()


class Wildcard(Button):
    """
    A combination of a logo (Wildcard) and a button that runs a function when clicked.
    """

    def __init__(self, x, y, texto, pantalla, font_size=25, key='star', size=None, on_click=None, on_click_param=None):
        Button.__init__(self, x, y, texto, pantalla,
                        font_size, on_click, on_click_param)

        self.logo = pg.image.load(config.get_key(key)).convert_alpha()
        if size is not None:
            self.logo = pg.transform.scale(self.logo, size)
        self.rect = self.logo.get_rect()
        logo_width, logo_height = self.rect.size
        self.rect.x = x - logo_width // 2
        self.rect.y = y - logo_height // 2
        self.is_disabled = False

        self.button_rect = self.image.get_rect(center=(x, y))
        self.logo_rect = self.rect
        self.wildcards_used_list = [0, 0, 0]

    def draw(self):
        self.pantalla.blit(self.logo, self.logo_rect)
        self.pantalla.blit(self.image, self.button_rect)

        if self.is_disabled:
            overlay = pg.Surface(self.rect.size)
            overlay.fill((65, 65, 65))
            overlay.set_alpha(160)
            self.pantalla.blit(overlay, self.rect.topleft)

    def update(self):
        self.draw()
        self.button_pressed()

    def set_disabled(self, disabled):
        self.is_disabled = disabled
