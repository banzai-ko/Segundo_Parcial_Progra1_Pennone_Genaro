import sys
import pygame as pg
from settings import SettingsLoader
from game.resources.scores import Ranking
from game.resources.menu import MenuManager

# Initialize configuration and ranking
config = SettingsLoader()
ranking = Ranking()


def run_game():
    """
    _summary_ Game main loop
    """

    pg.init()
    screen = pg.display.set_mode(config.screen, pg.SCALED)
    pg.display.set_caption('This or That')

    run = True
    file = config.get_key('RANK_FILE')
    lista = ranking.ranking(file)
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


# Run the game
run_game()
