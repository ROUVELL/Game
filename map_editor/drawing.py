import pygame as pg
from config import Config


class Drawing:
    def __init__(self, editor):
        self.editor = editor
        self.sc = editor.sc
        ##############
        self.fps_font = pg.font.SysFont('arial', 30)

    def bg(self):
        self.sc.fill('black')

    def world(self):
        [self.sc.blit(obj.image, obj.rect) for obj in self.editor.engine.world.current_world]

    def editing(self):
        if self.editor.engine.select_object:
            pg.draw.rect(self.sc, 'grey', self.editor.engine.select_object.rect, 1)

    def fps(self):
        fps = self.fps_font.render(f'{self.editor.clock.get_fps(): .1f}', True, Config.FPS_COLOR)
        self.sc.blit(fps, Config.FPS_POS)

    def all(self):
        self.bg()
        self.world()
        self.editing()
        self.fps()
