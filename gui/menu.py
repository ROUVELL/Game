import pygame as pg
from config import Config
import json


class Menu:
    def __init__(self, game):
        self.sc = game.sc
        self.clock = game.clock
        self.actived_func = None

    def load_screen(self):
        w, h = (Config.WIDTH * .4, Config.HEIGHT * .04)
        x, y = (Config.CENTER[0] - w // 2, Config.HEIGHT * .75 - h // 2)
        value = 0
        step = w / 100

        def load_screen_wrap():
            nonlocal value
            if value >= 100:
                print(value)
                self.actived_func = None
                return
            pg.draw.rect(self.sc, 'red', (x, y, step * value, h))
            pg.draw.rect(self.sc, 'green', (x, y, w, h), 2)
            value += .8

        self.actived_func = load_screen_wrap
        return self.run()

    def run(self):
        while self.actived_func:
            self.clock.tick(Config.FPS)
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        return False
                    if event.key == pg.K_RETURN:
                        return True

            self.sc.fill('black')
            self.actived_func()
            pg.display.flip()