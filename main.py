import pygame as pg
from Game.world import World
from Game.player import Player
from Game.camera import Camera
from Game.drawing import Drawing
from Game.config import Config


class Game:
    def __init__(self):
        pg.init()
        self.sc = pg.display.set_mode(Config.SCREEN, pg.SCALED | pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.running = True
        self.start()

    def start(self):
        self.world = World()
        self.player = Player(self)
        self.camera = Camera(self)
        self.draw = Drawing(self)

    def run(self):
        while self.running:
            self.clock.tick(Config.FPS)
            [exit() for event in pg.event.get() if event.type == pg.KEYUP and event.key == pg.K_ESCAPE]

            self.player.update()
            self.camera.update()
            self.draw.all()

            pg.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
