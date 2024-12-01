"""
_summary_ Mostrar color de la respuesta del publico
"""
import pygame as pg
from .widget import Widget


class Banner(Widget):
    """
    _summary_ Banner para mostrar el color de la elección de la audienci por pregunta.
    """

    def __init__(self, x, y, texto,  pantalla, font_size, color, size):
        super().__init__(x, y, texto, pantalla, font_size)
        self.rect = pg.rect.Rect((x, y), (size[0], size[1]))
        self.image = pg.surface.Surface(
            (self.rect.width, self.rect.height), pg.SRCALPHA)
        self.image.fill(color)

    def draw(self):
        """
        __summary__ Dibuja el banner en la pantalla
        """
        super().draw()

    def update(self):
        """
        _summary_ Actualiza la imagen del banner
        """
        self.draw()
