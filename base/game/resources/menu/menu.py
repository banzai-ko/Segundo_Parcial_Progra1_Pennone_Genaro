import pygame as pg

class Menu:
    
    forms_dict = {}
    
    def __init__(self, name: str, pantalla, x: int, y: int, active: bool, level_num: int, music_path: str):
        self.forms_dict[name] = self
        self.pantalla = pantalla
        self.active = active
        self.x = x
        self.y = y
        self.level_num = level_num
        self.music_path = music_path
    
    def set_active(self, name: str):
        for aux_form in self.forms_dict.values():
            aux_form.active = False
        self.forms_dict[name].active = True
        self.music_update()
    
    def music_update(self):
        pg.mixer.music.stop()
        pg.mixer.music.load(f'{self.music_path}')
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(-1, 0, 3000)
    
    def draw(self):
        self.pantalla.blit(self.surface, self.slave_rect)