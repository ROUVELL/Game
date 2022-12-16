import pygame as pg
from map import Map
from config import *


class Game:
    def __init__(self):
        pg.init()
        self.sc = pg.display.set_mode((WIDTH, HEIGHT), pg.NOFRAME)
        self.clock = pg.time.Clock()
        self.running = True
        self.start()

    def start(self):
        self.map = Map(self)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            [exit() if event.type == pg.KEYUP and event.key == pg.K_ESCAPE else None for event in pg.event.get()]

            self.sc.fill('black')
            self.map.draw_world()
            pg.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()