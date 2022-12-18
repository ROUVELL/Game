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
        self.engine.init()

    def run(self):
        while True:
            self.clock.tick(Config.FPS)
            [exit() for event in pg.event.get() if event.type == pg.KEYUP and event.key == pg.K_ESCAPE]

            self.engine.update()
            self.draw.all()
            pg.display.flip()


if __name__ == '__main__':
    app = App()
    app.run()
