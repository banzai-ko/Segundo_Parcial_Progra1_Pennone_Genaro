import pygame as pg


class Player:
    __instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self, nombre: str = 'Unknown Player', puntaje: int = 0):
        if not hasattr(self, 'initialized'):
            self.nombre = nombre
            self.puntaje = puntaje
            self.initialized = True
    
    @classmethod
    def get_player(cls):
        if cls.__instance is None:
            cls()

        return cls.__instance

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre: str):
        self.nombre = nombre
    
    def get_puntaje(self):
        return self.puntaje
    
    def set_puntaje(self, puntaje: int):
        self.puntaje = puntaje
        