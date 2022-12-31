import pygame as pg
from gui.button import Button
from config import Config


class UIEngine:
    def __init__(self):
        pg.init()
        self.sc = pg.display.set_mode(Config.SCREEN, pg.SCALED | pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.button = Button('Save World', Config.CENTER, lambda: print('Button pressed!'))

    def run(self):
        while 1:
            self.clock.tick(Config.FPS)
            [exit() for event in pg.event.get() if event.type == pg.KEYUP and event.key == pg.K_ESCAPE]
            self.sc.fill('black')
            self.button.update()
            self.button.draw(self.sc)
            pg.display.flip()


if __name__ == '__main__':
    engine = UIEngine()
    engine.run()
