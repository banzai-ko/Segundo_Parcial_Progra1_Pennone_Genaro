import pygame as pg
from game.resources.menu import Menu
from game.resources.scores import Ranking
from game.resources.player import Player
from game.resources.widgets import Button, TextBox, TextTitle
from settings import SettingsLoader

config = SettingsLoader()

DIMENSION_PANTALLA = config.screen
COLOR_BLANCO = config.get_key('COLOR_BLANCO')


class MenuEnterName(Menu):
    '''
    This class represents the enter name form  
    '''

    def __init__(self, name: str, pantalla: object, x: int, y: int, active: bool, level_num: int, music_name: str) -> None:

        super().__init__(name, pantalla, x, y, active, level_num, music_name)

        self.surface = pg.image.load(
            config.base_dir + config.get_key("GAME_OVER")
        ).convert_alpha()
        self.surface = pg.transform.scale(self.surface, DIMENSION_PANTALLA)
        self.slave_rect = self.surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y

        self.music_update()
        self.confirm_name = False
        self.ranking = Ranking.get_ranking()
        self.jugador = Player.get_player()
        self.score = self.jugador.get_puntaje()
        self.pantalla = pantalla
        print(f'SCORE: {self.score}')

        self.title = TextTitle(
            x=DIMENSION_PANTALLA[0] // 2,
            y=DIMENSION_PANTALLA[1] // 2-200,
            texto="GAME OVER",
            pantalla=pantalla,
            font_size=75
        )
        self.subtitle = TextTitle(
            x=DIMENSION_PANTALLA[0] // 2,
            y=DIMENSION_PANTALLA[1] // 70,
            texto="INGRESE SU NOMBRE:",
            pantalla=pantalla,
            font_size=50
        )
        self.subtitle_score = TextTitle(
            x=DIMENSION_PANTALLA[0] // 2,
            y=DIMENSION_PANTALLA[1] // 2 - 20,
            texto=f"PUNTAJE:{self.score}",
            pantalla=pantalla,
            font_size=30
        )

        self.text_box = TextBox(
            x=DIMENSION_PANTALLA[0] // 2,
            y=DIMENSION_PANTALLA[1] // 2 + 60,
            texto="_________________",
            pantalla=pantalla
        )

        self.button_confirm_name = Button(
            x=DIMENSION_PANTALLA[0] // 2,
            y=DIMENSION_PANTALLA[1] // 2 + 100,
            texto="CONFIRMAR NOMBRE",
            pantalla=pantalla,
            on_click=self.click_confirm_name,
            on_click_param='confirm'

        )

        self.button_exit = Button(
            x=100,
            y=700,
            texto="SALIR",
            pantalla=pantalla,
            on_click=self.set_exit,
            on_click_param='exit'
        )

        self.widget_list = [self.title, self.subtitle,
                            self.subtitle_score, self.button_confirm_name, self.button_exit]

    def click_confirm_name(self, parametro: str) -> None:
        '''
        Sets confirm name flag as True 
        Arguments: parametro (str)  
        Returns: None
        '''
        self.confirm_name = True
        self.jugador.set_nombre(self.text_box.writing)
        nombre = self.jugador.get_nombre()
        puntaje = self.jugador.get_puntaje()

        self.subtitle_score = TextTitle(
            x=DIMENSION_PANTALLA[0] // 2,
            y=DIMENSION_PANTALLA[1] // 2 - 20,
            texto=f"PUNTAJE:{self.score}",
            pantalla=self.pantalla,
            font_size=30
        )

        print(f'Nombre: {nombre}')
        print(f'Puntaje: {puntaje}')

        self.ranking.store_ranking((nombre, puntaje))
        self.widget_list = [self.title, self.button_exit, self.subtitle_score]

    def draw(self) -> None:
        '''
        Merges the elements of the form with the one from the main screen
        Arguments: None
        Returns: None
        '''
        super().draw()
        for widget in self.widget_list:
            widget.draw()
        self.text_box.draw()

    def set_exit(self, default_param='') -> None:
        pg.quit()

    def update(self, event_list) -> None:
        '''
        Executes the methods that need update 
        Arguments: event list (list)
        Returns: None
        '''
        super().draw()
        self.text_box.update(event_list)
        for widget in self.widget_list:
            widget.update()
