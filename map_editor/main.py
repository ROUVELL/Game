import pygame as pg
from map_editor.drawing import Drawing
from map_editor.engine import Engine
from config import Config


class Editor:
    def __init__(self):  # Потім вікно бути йти з Game
        pg.init()
        self.sc = pg.display.set_mode(Config.SCREEN, pg.SCALED | pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.draw = Drawing(self)
        self.engine = Engine(self)
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(Config.FPS)
            self.engine.update()
            self.draw.all()
            pg.display.flip()


if __name__ == '__main__':
    app = Editor()
    app.run()
