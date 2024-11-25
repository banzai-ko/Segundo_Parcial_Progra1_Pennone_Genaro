import pygame as pg
from .menu import Menu
from ..widgets import  (
    Button, TextTitle
)
from settings import SCREEN as DIMENSION_PANTALLA

class MenuRanking(Menu):
    
    def __init__(self, name, pantalla, x, y, active, level_num, music_path, ranking_list: list):
        super().__init__(name, pantalla, x, y, active, level_num, music_path)
        
        self.surface = pg.image.load('./game/assets/img/forms/form_ranking.png').convert_alpha()
        self.surface = pg.transform.scale(self.surface, DIMENSION_PANTALLA)
        self.slave_rect = self.surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y
        self.confirm_name = True
        
        self.ranking_on_screen = []
        self.ranking_list = ranking_list
        
        self.title = TextTitle(x=DIMENSION_PANTALLA[0]//2, y=DIMENSION_PANTALLA[1]//2-200, texto='This or that', pantalla=pantalla, font_size=75)
        self.subtitle = TextTitle(x=DIMENSION_PANTALLA[0]//2, y=DIMENSION_PANTALLA[1]//2-100, texto='TOP 10 Ranking', pantalla=pantalla, font_size=50)
        self.button_return_menu = Button(x=DIMENSION_PANTALLA[0]//2, y=DIMENSION_PANTALLA[1]//2+250, texto='VOLVER AL MENU', pantalla=pantalla, on_click=self.click_return_menu, on_click_param='form_main_menu')
        
        self.init_ranking()
        
        self.widget_list = [
            self.title, self.subtitle, self.button_return_menu
        ]
        self.music_update()
        
    
    def init_ranking(self):
        for i in range(len(self.ranking_list)):
            self.ranking_on_screen.append(
                TextTitle(x=DIMENSION_PANTALLA[0]//2-100,y=DIMENSION_PANTALLA[1]//2.5+i*25, texto=f'{i+1}', pantalla=self.pantalla, font_size=25)
            )
            
            self.ranking_on_screen.append(
                TextTitle(x=DIMENSION_PANTALLA[0]//2,y=DIMENSION_PANTALLA[1]//2.5+i*25, texto=f'{self.ranking_list[i][0]}', pantalla=self.pantalla, font_size=25)
            )
            
            self.ranking_on_screen.append(
                TextTitle(x=DIMENSION_PANTALLA[0]//2+100,y=DIMENSION_PANTALLA[1]//2.5+i*25, texto=f'{self.ranking_list[i][1]}', pantalla=self.pantalla, font_size=25)
            )
    
    def click_return_menu(self, parametro):
        self.set_active(parametro)
    
    def draw(self):
        super().draw()
        for widget in self.widget_list:
            widget.draw()
        for ranking in self.ranking_on_screen:
            ranking.draw()
    
    def update(self):
        super().draw()
        for widget in self.widget_list:
            widget.update()