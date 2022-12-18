import pygame as pg
from drawing import Drawing
from parser import Parser
from engine import Engine
from config import Config


class Editor:
    def __init__(self):
        pg.init()
        self.sc = pg.display.set_mode(Config.SCREEN, pg.NOFRAME)
        self.clock = pg.time.Clock()
        self.parser = Parser()
        self.draw = Drawing(self)
        self.engine = Engine(self)

    def run(self):
        while True:
            self.clock.tick(Config.FPS)
            [exit() for event in pg.event.get() if event.type == pg.KEYUP and event.key == pg.K_ESCAPE]

            self.engine.update()
            self.draw.all()
            pg.display.flip()


if __name__ == '__main__':
    editor = Editor()
    editor.run()
