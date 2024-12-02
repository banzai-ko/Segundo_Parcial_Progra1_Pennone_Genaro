import pygame as pg
from settings import SettingsLoader
from .widget import Widget

config = SettingsLoader()
COLOR_BLANCO = config.get_key('COLOR_BLANCO')
COLOR_BLANCO = tuple(map(int, COLOR_BLANCO.strip('()').split(', ')))
SONIDO_SELECT = config.base_dir + config.get_key('SONIDO_SELECT')
BUBBLE_BOBBLE = config.get_key('BUBBLE_BOBBLE')


class AnswerButton(Widget):
    """
    Clase Botones de Respuestas con Wrapper

    Arguments:
        Widget -- Hereda de la clase Widget
    """

    def __init__(self, x, y, texto, pantalla, font_size=25, on_click=None, on_click_param=None, max_width=450):
        super().__init__(x, y, texto, pantalla, font_size)
        self.font = pg.font.Font(BUBBLE_BOBBLE, self.font_size)
        self.texto = texto
        self.max_width = max_width
        self.lines = self.wrap_text(self.texto)
        self.image = self.render_text(self.lines)
        self.rect = self.image.get_rect()

        # Ensure the text is always centered based on the image's width and height
        self.rect.center = (x, y)

        self.click_option_sfx = pg.mixer.Sound(SONIDO_SELECT)
        self.on_click = on_click
        self.on_click_param = on_click_param

    def wrap_text(self, text):
        """
        Wrapper para que no exceda el ancho maximo
        """
        lines = []
        words = text.split(' ')
        current_line = ''

        for word in words:
            test_line = current_line + ' ' + word if current_line else word
            test_surface = self.font.render(test_line, True, COLOR_BLANCO)

            if test_surface.get_width() <= self.max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def render_text(self, lines):
        """
        Render the wrapped text, ensuring it's centered.
        """
        line_height = self.font.get_height()
        total_height = line_height * len(lines)
        text_surface = pg.Surface((self.max_width, total_height), pg.SRCALPHA)

        y_offset = 0
        for line in lines:
            line_surface = self.font.render(line, True, COLOR_BLANCO)
            # Center the text horizontally by calculating the offset
            x_offset = (self.max_width - line_surface.get_width()) // 2
            text_surface.blit(line_surface, (x_offset, y_offset))
            y_offset += line_height

        return text_surface

    def button_pressed(self):
        """
        Handler click del botón
        """
        mouse_pos = pg.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 1:
                pg.time.delay(300)
                self.on_click(self.on_click_param)
                self.click_option_sfx.set_volume(0.4)
                self.click_option_sfx.play()

    def draw(self):
        super().draw()

    def update(self):
        self.draw()
        self.button_pressed()
