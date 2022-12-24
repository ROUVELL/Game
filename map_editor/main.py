import pygame as pg
from drawing import Drawing
from engine import Engine
from config import Config


class App:
    def __init__(self):
        pg.init()
        self.sc = pg.display.set_mode(Config.SCREEN, pg.NOFRAME)
        self.clock = pg.time.Clock()
        self.draw = Drawing(self)
        self.engine = Engine(self)

    def run(self):
        while True:
            self.clock.tick(Config.FPS)

            self.engine.update()
            self.draw.all()
            pg.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
