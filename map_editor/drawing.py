import pygame as pg
from config import Config


class Drawing:
    def __init__(self, app):
        self.app = app
        self.sc = app.sc
        ##############
        self.fps_font = pg.font.SysFont('arial', 30)

    def bg(self):
        self.sc.fill('black')

    def world(self):
        [self.sc.blit(obj.image, obj.rect) for obj in self.app.engine.world.current_world]

    def fps(self):
        fps = self.fps_font.render(f'{self.app.clock.get_fps(): .1f}', True, Config.FPS_COLOR)
        self.sc.blit(fps, Config.FPS_POS)

    def all(self):
        self.bg()
        self.world()
        self.fps()
