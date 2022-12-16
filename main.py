import pygame as pg
from config import *


class Game:
    def __init__(self):
        pg.init()
        self.sc = pg.display.set_mode((WIDTH, HEIGHT), pg.NOFRAME)
        self.clock = pg.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            [exit() if event.type == pg.KEYUP and event.key == pg.K_ESCAPE else None for event in pg.event.get()]

            self.sc.fill('black')
            pg.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()