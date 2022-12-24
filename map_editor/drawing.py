import pygame as pg
from config import Config


class Drawing:
    def __init__(self, app):
        self.app = app
        self._sc = app.sc
        ##############
        self._fps_font = pg.font.SysFont('arial', 30)

    def bg(self):
        self._sc.fill('black')

    def world(self):
        [self._sc.blit(obj.image, obj.rect) for obj in self.app.engine.parser.current_world]

    def tabs(self):
        self.app.engine.objects_list.draw_on_screen()
        self.app.engine.editor.draw_on_screen()

    def fps(self):
        fps = self._fps_font.render(f'{self.app.clock.get_fps(): .1f}', True, Config.FPS_COLOR)
        self._sc.blit(fps, Config.FPS_POS)

    def all(self):
        self.bg()
        self.world()
        self.tabs()
        self.fps()
