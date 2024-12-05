import pygame as pg
from settings import SettingsLoader
from .menu_main import MainMenu
from .menu_game import MenuGame
from .menu_pause import MenuPause
from .menu_ranking import MenuRanking
from .menu_options import MenuOptions
from .menu_enter_name import MenuEnterName

config = SettingsLoader()

DIMENSION_PANTALLA = config.screen
SONIDO_MUSIC = config.get_key('SONIDO_MUSIC')
SONIDO_MENU = config.get_key('SONIDO_MENU')
SONIDO_OPCIONES = config.get_key('SONIDO_OPCIONES')
SONIDO_RANKING = config.get_key('SONIDO_RANKING')


class MenuManager:
    """
    _summary_ Handler de menus
    """

    FORM_ENTER_NAME = 4
    FORM_LEVEL = 3
    FORM_MAIN = 0
    exit_requested = False

    def __init__(self, pantalla, ranking_db=None):

        self.main_screen = pantalla
        self.ranking_db = ranking_db
        self.current_level = 0

        self.forms = [
            MainMenu(
                name='form_main_menu',
                pantalla=self.main_screen,
                x=0,
                y=0,
                active=True,
                level_num=1,
                music_path=SONIDO_MENU
            ),
            MenuRanking(
                name='form_rankings',
                pantalla=self.main_screen,
                x=0,
                y=0,
                active=True,
                level_num=1,
                music_path=SONIDO_RANKING,
                ranking_list=self.ranking_db
            ),
            MenuOptions(
                name='form_options',
                pantalla=self.main_screen,
                x=0,
                y=0,
                active=True,
                level_num=1,
                music_path=SONIDO_OPCIONES
            ),
            MenuPause(
                name="form_pause",
                pantalla=self.main_screen,
                x=0,
                y=0,
                active=True,
                level_num=self.current_level,
                music_name=SONIDO_MUSIC),
            MenuEnterName(
                name="form_enter_name",
                pantalla=self.main_screen,
                x=0,
                y=0,
                active=True,
                level_num=1,
                music_name=SONIDO_MENU,
            ),
            MenuGame(
                name="form_game",
                pantalla=self.main_screen,
                x=0,
                y=0,
                active=True,
                level_num=1,
                music_path=SONIDO_MENU
            )

        ]

    def keys_update(self, event_list: list) -> None:
        '''
        Checks if ESC key is pressed to acces the Pause Menu
        Arguments: event list (list)
        Returns: None
        '''

        for event in event_list:

            if (event.type == pg.KEYDOWN):
                if (event.key == pg.K_ESCAPE):
                    self.forms[3].set_active("form_pause")
            elif event.type == pg.QUIT:  # Handle window close button
                self.exit_game()

    def forms_update(self, event_list: list):
        """Update and draw active forms"""
        for index, form in enumerate(self.forms):
            if not form.active:
                continue

            if index == self.FORM_ENTER_NAME:
                form.update(event_list)
            else:
                form.update()

            form.draw()

            # Check if main menu form requests exit
            if index == self.FORM_MAIN and getattr(form, 'exit_requested', False):
                self.exit_game()

            if index == self.FORM_LEVEL and form.level_restart:

                pass

            break

    def update(self, event_list: list):
        self.keys_update(event_list)
        self.forms_update(event_list)
