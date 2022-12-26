import pygame as pg
from config import Config


class Drawing:
    def __init__(self, app):
        self.app = app
        self._sc = app.sc
        ##############
        self._fps_font = pg.font.SysFont('arial', 30)  # Можна було б щось гарніше
        self._world_sc = pg.Surface((Config.DOUBLE_WIDTH, Config.DOUBLE_HEIGHT), pg.SRCALPHA)
        self._world_sc_rect = self._world_sc.get_rect(center=Config.CENTER)

    def bg(self):
        self._sc.fill('black')

    def world(self):
        self._world_sc.fill('black')
        [self._world_sc.blit(obj.image, obj.rect) for obj in self.app.engine.parser.current_world]
        scaled_world = self._world_sc
        if self.app.engine.parser.need_scaling:
            coeff = self.app.engine.parser.scale_coeff
            w, h = self._world_sc_rect.width * coeff, self._world_sc_rect.height * coeff
            scaled_world = pg.transform.scale(self._world_sc, (w, h))
            self._world_sc_rect = scaled_world.get_rect(center=Config.CENTER)
            self.app.engine.parser.need_scaling = False
        self._sc.blit(scaled_world, self._world_sc_rect)

    def tabs(self):
        self.app.engine.objects_list.draw()
        self.app.engine.editor.draw_on_screen()

    def fps(self):
        fps = self._fps_font.render(f'{self.app.clock.get_fps(): .1f}', True, Config.FPS_COLOR)
        self._sc.blit(fps, Config.FPS_POS)

    def all(self):
        self.bg()
        self.world()
        self.tabs()
        self.fps()
