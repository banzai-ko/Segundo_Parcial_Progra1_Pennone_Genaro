import pygame as pg
from .menu import Menu
from ..widgets import (
    Button, TextTitle
)
from settings import SCREEN as DIMENSION_PANTALLA

class MenuPause(Menu):
    def __init__(self,name:str,pantalla:object,x:int,y:int,active:bool,level_num:int,music_name:str)->None:
        '''
        This class represents the pause form  
        '''
        super().__init__(name,pantalla,x,y,active,level_num,music_name)
        self.level_restart = False
        self.current_level_number = level_num
        self.paused = pg.mixer.music.get_busy() 

        self.surface = pg.image.load('./game/assets/img/forms/form_pause.png').convert_alpha()
        self.surface = pg.transform.scale(self.surface, DIMENSION_PANTALLA)
        self.slave_rect = self.surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y

        self.menu_ppal_title = TextTitle(x=DIMENSION_PANTALLA[0]//2,y=DIMENSION_PANTALLA[1]//2-200,texto="This or that",pantalla=pantalla,font_size=75)
        self.menu_ppal_subtitle = TextTitle(x=DIMENSION_PANTALLA[0]//2,y=DIMENSION_PANTALLA[1]//2-150,texto="PAUSA",pantalla=pantalla,font_size=50)

        self.button_resume = Button(x=DIMENSION_PANTALLA[0]//2,y=DIMENSION_PANTALLA[1]//2-70,texto="VOLVER AL NIVEL",pantalla=pantalla,on_click=self.click_resume,on_click_param="form_start_level")
        self.button_restart = Button(x=DIMENSION_PANTALLA[0]//2,y=DIMENSION_PANTALLA[1]//2,texto="REINICIAR NIVEL",pantalla=pantalla,on_click=self.click_restart,on_click_param="form_start_level")
        self.button_music = Button(x=DIMENSION_PANTALLA[0]//2,y=DIMENSION_PANTALLA[1]//2+70,texto="MUSICA: ON/OFF",pantalla=pantalla,on_click=self.click_music)
        self.button_return_menu = Button(x=DIMENSION_PANTALLA[0]//2,y=DIMENSION_PANTALLA[1]//2+150,texto="VOLVER AL MENU",pantalla=pantalla,on_click=self.click_return_menu,on_click_param="form_main_menu")
        
        self.widget_list = [self.menu_ppal_subtitle,self.menu_ppal_title,self.button_resume,
        self.button_restart,self.button_music,self.button_return_menu]
           
       
    def click_resume(self,parametro:str)->None:  
        '''
        Sets active start level form and sets level number 
        Arguments: parametro (str)  
        Returns: None
        '''  
        self.set_active(parametro)
        
        
    def click_restart(self,parametro:str)->None:
        '''
        Sets active start level form and sets level number 
        Arguments: parametro (str)  
        Returns: None
        '''   
        self.set_active(parametro)
        self.level_restart = True
                

    def click_music(self,parametro:str)->None:
        '''
        Sets active start level form and sets level number 
        Arguments: parametro (str)  
        Returns: None
        '''  
        if self.paused:
            pg.mixer.music.unpause()
        elif not self.paused:
            pg.mixer.music.pause()
        self.paused = not self.paused
        
    def click_return_menu(self,parametro:str)->None: 
        '''
        Sets active start level form and sets level number 
        Arguments: parametro (str)  
        Returns: None
        '''  
        self.set_active(parametro)
            
    def draw(self)->None:
        '''
        Merges the elements of the form with the one from the main screen
        Arguments: None
        Returns: None
        '''
        for widget in self.widget_list:    
            widget.draw()

    def update(self)->None:
        '''
        Executes the methods that need update 
        Arguments: event list (list)
        Returns: None
        '''
        super().draw()
        for widget in self.widget_list:    
            widget.update()
