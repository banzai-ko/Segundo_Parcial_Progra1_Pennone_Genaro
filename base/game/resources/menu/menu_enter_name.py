import pygame as pg
from .menu import Menu
from ..widgets import Button, TextBox, TextTitle
from settings import SCREEN as DIMENSION_PANTALLA, COLOR_BLANCO

class MenuEnterName(Menu):
    '''
    This class represents the enter name form  
    '''
    def __init__(self, name:str, pantalla:object, x:int, y:int, active:bool, level_num:int, music_name:str, score:int)->None:
        super().__init__(name,pantalla,x,y,active,level_num,music_name)

        self.surface = pg.image.load('./game/assets/img/forms/form_enter_name.png').convert_alpha()
        self.surface = pg.transform.scale(self.surface, DIMENSION_PANTALLA)
        self.slave_rect = self.surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y
        self.score = score
      
        self.music_update()
        self.confirm_name = False
                   
        self.title = TextTitle(x=DIMENSION_PANTALLA[0]//2,y=DIMENSION_PANTALLA[1]//2-200,texto="This or that",pantalla=pantalla,font_size=75)
        self.subtitle = TextTitle(x=DIMENSION_PANTALLA[0]//2,y=DIMENSION_PANTALLA[1]//2-90,texto="INGRESE SU NOMBRE:",pantalla=pantalla,font_size=50)
        self.subtitle_score = TextTitle(x=DIMENSION_PANTALLA[0]//2,y=DIMENSION_PANTALLA[1]//2-20,texto=f"PUNTAJE:{score}",pantalla=pantalla,font_size=30)
        
        self.text_box = TextBox(x=DIMENSION_PANTALLA[0]//2,y=DIMENSION_PANTALLA[1]//2+40,texto="_________________",pantalla=pantalla)
        self.button_confirm_name = Button(x=DIMENSION_PANTALLA[0]//2,y=DIMENSION_PANTALLA[1]//2+100,texto="CONFIRMAR NOMBRE",pantalla=pantalla
        ,on_click=self.click_confirm_name)
        
        self.widget_list = [self.title, self.subtitle,self.subtitle_score,self.button_confirm_name]

        
    def click_confirm_name(self,parametro:str)->None: 
        '''
        Sets confirm name flag as True 
        Arguments: parametro (str)  
        Returns: None
        '''  
        self.confirm_name = True
        print(f'Su nombre: {self.writing_text.text} - {self.score} puntos')
        
        def draw(self):
            super().draw()
        
            for widget in self.widget_list:
                widget.draw()
            
            self.text_box.draw()
            
            if not hasattr(self, 'writing_text'):
                self.writing_text = TextTitle(
                    x=DIMENSION_PANTALLA[0] // 2,
                    y=DIMENSION_PANTALLA[1] // 2 + 30,
                    text="",
                    pantalla=self.master_surface,
                    font_size=30
                )
            
            self.writing_text.text = self.text_box.writing.upper()
            self.writing_text.draw()


    def update(self)->None:
        '''
        Executes the methods that need update 
        Arguments: event list (list)
        Returns: None
        '''
        self.draw()
        for widget in self.widget_list:    
            widget.update()  

