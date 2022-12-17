import pygame as pg
from object_handler import ObjectHandler
from config import Config


class Game:
    def __init__(self):
        pg.init()
        self.sc = pg.display.set_mode(Config.SCREEN, pg.NOFRAME)
        self.clock = pg.time.Clock()
        self.running = True
        self.start()

    def start(self):
        self.object_handler = ObjectHandler(self)

    def run(self):
        while self.running:
            self.clock.tick(Config.FPS)
            [exit() if event.type == pg.KEYUP and event.key == pg.K_ESCAPE else None for event in pg.event.get()]

            self.sc.fill('black')
            self.object_handler.draw_world()
            pg.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()