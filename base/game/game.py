import sys
import pygame as pg

from game.resources import module

from game.resources.menu import (
    MenuManager
    )
from game.resources.scores import ranking
from settings import SCREEN, RANK_FILE



def run_game():
    pg.init()

    screen = pg.display.set_mode(SCREEN, pg.SCALED)
    pg.display.set_caption('This or That')
    
    run = True
    
    lista = ranking(RANK_FILE)
    
    menu = MenuManager(screen, lista)
    
    while run:
        event_list = pg.event.get()
        for event in event_list:
            if event.type == pg.QUIT:
                run = False
            
        
        menu.update(event_list)
        pg.display.update()
    pg.quit()
    sys.exit()