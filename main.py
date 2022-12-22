import pygame as pg
from world import World
from player import Player
from camera import Camera
from drawing import Drawing
from config import Config


class Game:
    def __init__(self):
        pg.init()
        self.sc = pg.display.set_mode(Config.SCREEN, pg.NOFRAME)
        self.clock = pg.time.Clock()
        self.start()
        print((f'{Config.WIDTH / 4}'))

    def start(self):
        self.world = World()
        self.player = Player(self)
        self.camera = Camera(self)
        self.draw = Drawing(self)

    def update(self):
        self.player.update()
        self.camera.update()

    def run(self):
        while True:
            self.clock.tick(Config.FPS)
            [exit() for event in pg.event.get() if event.type == pg.KEYUP and event.key == pg.K_ESCAPE]

            self.update()
            self.draw.all()

            pg.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()