import pygame as pg
from .widget import Widget
from settings import SettingsLoader
config = SettingsLoader()
COLOR_BLANCO = config.get_key('COLOR_BLANCO')
COLOR_BLANCO = tuple(map(int, COLOR_BLANCO.strip('()').split(', ')))


class TextBox(Widget):

    def __init__(self, x, y, texto, pantalla, font_size=25, on_click=None, on_click_param=None):
        super().__init__(x, y, texto, pantalla, font_size)

        # Set up font and initial text rendering
        self.font = pg.font.Font(
            config.get_key('BUBBLE_BOBBLE'), self.font_size)
        self.image = self.font.render(
            self.texto, True, COLOR_BLANCO)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # TextBox-specific attributes
        self.click_option_sfx = pg.mixer.Sound(config.base_dir +
                                               config.get_key('SONIDO_SELECT'))
        self.click_option_sfx.set_volume(0.3)

        self.on_click = on_click
        self.on_click_param = on_click_param

        self.write_on = True  # Enable writing
        
        self.box_width = 200  # Add a fixed width for the textbox
        self.writing = ''
        self.image_writing = self.font.render(self.writing, True, COLOR_BLANCO)
        self.rect_writing = self.image_writing.get_rect()
        self.rect_writing.centerx = x  # Center horizontally at x
        self.rect_writing.centery = y - 10  # Offset vertically
 
    def write_on_box(self, event_list):
        for evento in event_list:
            if evento.type == pg.KEYDOWN and self.write_on:
                if evento.key == pg.K_BACKSPACE:
                    self.writing = self.writing[:-1]
                else:
                    self.writing += evento.unicode

                self.click_option_sfx.play()

                # Update the writing surface
                self.image_writing = self.font.render(
                    self.writing, True, COLOR_BLANCO)
                self.rect_writing = self.image_writing.get_rect()
                self.rect_writing.centerx = self.x  # Keep centered at original x position
                self.rect_writing.centery = self.y - 10

    def draw(self):
        """Draw the text box and user input to the screen."""
        # Draw the static text
        self.pantalla.blit(self.image, self.rect)

        # Draw the dynamic user input
        self.pantalla.blit(self.image_writing, self.rect_writing)

    def update(self, event_list):
        """Update the text box based on events and redraw it."""
        self.write_on_box(event_list)
        self.draw()
