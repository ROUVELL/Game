import pygame as pg
from world import World
from player import Player
from camera import Camera
from config import Config


class Game:
    def __init__(self):
        pg.init()
        self.sc = pg.display.set_mode(Config.SCREEN, pg.NOFRAME)
        self.clock = pg.time.Clock()
        self.running = True
        self.start()

    def start(self):
        self.world = World(self)
        self.player = Player(self)
        self.camera = Camera(self)

    def update(self):
        self.player.update()

    def draw(self):
        self.sc.fill('black')
        self.world.draw_world()
        self.player.draw()

    def run(self):
        while self.running:
            self.clock.tick(Config.FPS)
            [exit() if event.type == pg.KEYUP and event.key == pg.K_ESCAPE else None for event in pg.event.get()]

            self.update()
            self.draw()

            pg.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()