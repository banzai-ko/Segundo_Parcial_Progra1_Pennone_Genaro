import pygame as pg
from settings import SettingsLoader

config = SettingsLoader()


def str_to_bool(s):
    """
    _summary_ Convierte una cadena a un booleano, settings config desde archivo ini
    """
    return True if s == "True" else False if s == "False" else None


class Menu:

    """
    _summary_ Clase Padre Menu
    """

    forms_dict = {}

    def __init__(self, name: str, pantalla, x: int, y: int, active: bool, level_num: int, music_path: str):
        self.forms_dict[name] = self
        self.pantalla = pantalla
        self.active = active
        self.x = x
        self.y = y
        self.level_num = level_num
        self.music_path = config.base_dir + music_path

    def set_active(self, name: str):
        """
        _summary_ Cambia estado elementos

        Arguments:
            name -- _Nombre elemento a activar
        """
        for aux_form in self.forms_dict.values():
            aux_form.active = False
        self.forms_dict[name].active = True
        self.music_update()

    def music_update(self):
        """
        _summary_ Actualiza el estado de la musica
        """
        if config.str_to_bool(config.get_key('MUSIC')):
            pg.mixer.music.stop()
            pg.mixer.music.load(f'{self.music_path}')
            pg.mixer.music.set_volume(0.3)
            pg.mixer.music.play(-1, 0, 3000)

    def draw(self):
        """
        _summary_ Dibuja el Menu
        """
        self.pantalla.blit(self.surface, self.slave_rect)
