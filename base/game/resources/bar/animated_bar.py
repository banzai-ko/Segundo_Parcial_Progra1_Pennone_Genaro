import pygame as pg
from game.resources.widgets.widget import Widget


class AnimatedBar(Widget):
    """
    Clase para mostrar barra animada
    """

    def __init__(self, x, y, texto, pantalla, data, font_size=25, bar_height=55, total_length=350, image=None):
        super().__init__(x, y, texto, pantalla, font_size)

        self.data = data
        self.pantalla = pantalla
        self.bar_height = bar_height
        self.total_length = total_length
        self.image = image
        self.active = False

        self.red_length = 0
        self.blue_length = 0
        self.target_red_length = 0
        self.target_blue_length = 0
        self.animation_speed = 5

        if self.image:
            self.image = pg.transform.scale(
                self.image, (total_length + 30, bar_height + 60))
            self.rect = self.image.get_rect(center=(x, y + 25))

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

        if total_elements > 0:
            self.target_red_length = (
                self.num_zeros / total_elements) * self.total_length
            self.target_blue_length = (
                self.num_ones / total_elements) * self.total_length
        else:
            self.target_red_length = 0
            self.target_blue_length = 0

    def animate(self):
        """
        Barras Animadas 
        """
        if self.red_length < self.target_red_length:
            self.red_length += self.animation_speed
            if self.red_length > self.target_red_length:
                self.red_length = self.target_red_length

        if self.red_length > self.target_red_length:
            self.red_length -= self.animation_speed
            if self.red_length < self.target_red_length:
                self.red_length = self.target_red_length

        if self.blue_length < self.target_blue_length:
            self.blue_length += self.animation_speed
            if self.blue_length > self.target_blue_length:
                self.blue_length = self.target_blue_length

        if self.blue_length > self.target_blue_length:
            self.blue_length -= self.animation_speed
            if self.blue_length < self.target_blue_length:
                self.blue_length = self.target_blue_length

    def draw(self):
        """
        Dibujar barra animada
        """
        if self.image and self.active:
            self.pantalla.blit(self.image, self.rect.topleft)

            self.animate()

            total_bar_length = self.red_length + self.blue_length
            center_x = self.x - total_bar_length // 2

            pg.draw.rect(
                self.pantalla,
                (255, 0, 0),
                (
                    center_x,
                    self.y,
                    self.red_length,
                    self.bar_height
                )
            )

            pg.draw.rect(
                self.pantalla,
                (0, 0, 255),
                (
                    center_x + self.red_length,
                    self.y,
                    self.blue_length,
                    self.bar_height
                )
            )

    def set_active(self, active_value):
        """
        Set para mostrar u ocultar la barra animada

        Args:
            active_value (bool): Recibe booleano para activar o desactivar
        """
        self.active = active_value
