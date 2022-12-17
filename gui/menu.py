import pygame as pg
from config import Config
import json


class Menu:
    def __init__(self, game):
        self.sc = game.sc
        self.clock = game.clock
        self.running = True
        self._parse()

    @staticmethod
    def _get_config():
        with open(Config.MENU, encoding='utf-8') as file:
            config = json.load(file)
        return config

    def _parse(self):
        config = self._get_config()
        print(config)

    def draw(self):
        pass

    def start_menu(self):
        while self.running:
            self.clock.tick(Config.FPS)
            for event in pg.event.get():
                if event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                    return False

            self.sc.fill('black')
            # self.draw()
            pg.display.flip()