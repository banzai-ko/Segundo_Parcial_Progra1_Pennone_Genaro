import pygame as pg
from .widget import Widget
from settings import COLOR_AZUL, SONIDO_SELECT, BUBBLEBOY

class TextBox(Widget):
    
    def __init__(self, x, y, texto, pantalla, font_size=25, on_click=None, on_click_param=None):
        super().__init__(x, y, texto, pantalla, font_size)
        
        # Set up font and initial text rendering
        self.font = pg.font.Font(BUBBLEBOY, self.font_size)
        self.image = self.font.render(self.texto, True, COLOR_AZUL)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # TextBox-specific attributes
        self.click_option_sfx = pg.mixer.Sound(SONIDO_SELECT)
        self.click_option_sfx.set_volume(0.3)
        
        self.on_click = on_click
        self.on_click_param = on_click_param
        
        self.write_on = True  # Enable writing
        self.writing = ''  # Dynamic user input
        self.image_writing = self.font.render(self.writing, True, COLOR_AZUL)
        self.rect_writing = self.image_writing.get_rect()
        self.rect_writing.center = (x, y + 30)  # Adjust position below initial text
        
    def write_on_box(self, event_list):
        """Handle user input for the TextBox."""
        for evento in event_list:
            if evento.type == pg.KEYDOWN and self.write_on:
                if evento.key == pg.K_BACKSPACE:  # Remove last character
                    self.writing = self.writing[:-1]
                else:  # Add new character
                    self.writing += evento.unicode
                
                # Play sound for key press
                self.click_option_sfx.play()
                
                # Update the writing surface
                self.image_writing = self.font.render(self.writing, True, COLOR_AZUL)
    
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
