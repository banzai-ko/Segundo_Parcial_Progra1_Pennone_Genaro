import pygame as pg
from settings import SettingsLoader
from ..widgets import (
    Button, TextTitle
)
from .menu import Menu
config = SettingsLoader()


DIMENSION_PANTALLA = config.screen


class MenuRanking(Menu):
    """
    _summary_ Clase MenuRanking Muestra Menu Ranking

    Arguments:
        Menu -- _Clase Padre Menu_
    """

    def __init__(self, name, pantalla, x, y, active, level_num, music_path, ranking_list: list):
        super().__init__(name, pantalla, x, y, active, level_num, music_path)

        self.surface = pg.image.load(
            config.base_dir + config.get_key('RANKING_BACKGROUND')).convert_alpha()
        self.surface = pg.transform.scale(self.surface, DIMENSION_PANTALLA)
        self.slave_rect = self.surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y
        self.confirm_name = True

        self.ranking_on_screen = []
        self.ranking_list = ranking_list

        self.subtitle = TextTitle(
            x=DIMENSION_PANTALLA[0]//2, y=DIMENSION_PANTALLA[1]//2-300, texto='TOP 10 Ranking', pantalla=pantalla, font_size=50)
        self.button_return_menu = Button(x=DIMENSION_PANTALLA[0]//2, y=DIMENSION_PANTALLA[1]//2+250, texto='VOLVER AL MENU',
                                         pantalla=pantalla, on_click=self.click_return_menu, on_click_param='form_main_menu')

        self.init_ranking()

        self.widget_list = [
            self.subtitle, self.button_return_menu
        ]
        self.music_update()

    def init_ranking(self):
        for i in range(len(self.ranking_list)):

            self.ranking_on_screen.append(
                TextTitle(x=DIMENSION_PANTALLA[0]//2, y=DIMENSION_PANTALLA[1]//2.5+i*25, texto=f'{
                          self.ranking_list[i][0]}', pantalla=self.pantalla, font_size=25)
            )

            self.ranking_on_screen.append(
                TextTitle(x=DIMENSION_PANTALLA[0]//2+100, y=DIMENSION_PANTALLA[1]//2.5+i*25 - 150, texto=f'{
                          self.ranking_list[i][1]}', pantalla=self.pantalla, font_size=25)
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
