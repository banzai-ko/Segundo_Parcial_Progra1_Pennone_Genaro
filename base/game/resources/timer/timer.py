import pygame as pg
from pygame.time import get_ticks


class GameTimer:
    """
    _summary_ Clase Timer para manejo de cronometro
    """

    def __init__(self, duration):
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.elapsed_time = 0

    def activate(self):
        self.active = True
        self.start_time = get_ticks()
        self.elapsed_time = 0

    def deactivate(self):
        self.active = False
        self.start_time = 0
        self.elapsed_time = 0

    def update(self):
        if self.active:
            current_time = get_ticks()
            print(f'Timer: {current_time}')
            print(f'Start: {self.start_time}')
            print(f'Difference: {current_time - self.start_time}')
            print(f'Duration: {self.duration}')
            self.elapsed_time = current_time - self.start_time
            if self.elapsed_time >= self.duration:
                self.deactivate()
