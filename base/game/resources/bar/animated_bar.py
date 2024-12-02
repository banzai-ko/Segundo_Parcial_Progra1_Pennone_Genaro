import pygame as pg
from game.resources.widgets.widget import Widget


class AnimatedBar(Widget):
    """
      Clase para mostrar barra animada
    """

    def __init__(self, x, y, texto, pantalla, data, font_size=25, bar_height=50, total_length=600, image=None):

        super().__init__(x, y, texto, pantalla, font_size)

        self.data = data
        self.bar_height = bar_height
        self.total_length = total_length
        self.image = image

        if self.image:
            self.image = pg.transform.scale(
                self.image, (500, bar_height+20))
            self.rect = self.image.get_rect(center=(x, y+25))

        self.num_zeros = self.data.count(0)
        print(f'RED {self.num_zeros}')
        self.num_ones = self.data.count(1)
        print(f'BLUE {self.num_ones}')

        self.update()

    def update(self):
        """
        Actualizar con datos
        """
        total_elements = self.num_zeros + self.num_ones
        self.red_length = ((self.num_zeros / total_elements) *
                           100)*2
        self.blue_length = ((self.num_ones / total_elements) *
                            100) * 2

    def draw(self):
        """
        Versus Bar
        """
        if self.image:
            self.pantalla.blit(self.image, self.rect.topleft)

        pg.draw.rect(self.pantalla, (255, 0, 0),
                     (self.x - 250, self.y, self.red_length, self.bar_height))

        pg.draw.rect(self.pantalla, (0, 0,
                                     255), (self.x +
                     self.red_length - 250, self.y, self.blue_length, self.bar_height))
