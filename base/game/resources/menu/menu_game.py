import pygame as pg
from .menu import Menu
from ..widgets import (
    Button, TextTitle
)
from settings import SCREEN as DIMENSION_PANTALLA

class MenuGame(Menu):
    
    def __init__(self, name, pantalla, x, y, active, level_num, music_path):
        super().__init__(name, pantalla, x, y, active, level_num, music_path)
        
        self.surface = pg.image.load('./game/assets/img/game.png').convert_alpha()
        self.surface = pg.transform.scale(self.surface, DIMENSION_PANTALLA)
        
        self.slave_rect = self.surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y
        
        
        
        self.button_back = Button(x=120, y=DIMENSION_PANTALLA[1]//2+300, texto='VOLVER AL MENU', pantalla=pantalla, on_click=self.click_back, on_click_param='form_main_menu')
        self.widgets_list = [
            self.button_back, 
        ]
        self.music_update()
        
    def click_music_on(self, parametro):
        pg.mixer.music.unpause()
    
    def click_music_off(self, parametro):
        pg.mixer.music.pause()
    
    def click_back(self, parametro):
        self.set_active(parametro)
    
    def draw(self):
        super().draw()
        for widget in self.widgets_list:
            widget.draw()
        
    def update(self):
        super().draw()
        for widget in self.widgets_list:
            widget.update()