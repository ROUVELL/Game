import pygame as pg
from config import Config


class Drawing:
    def __init__(self, app):
        self.app = app
        self._sc = app.sc
        ##############
        self.internal_surf = pg.Surface(Config.INTERNAL_SURFACE_SIZE, pg.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=Config.CENTER)
        self.internal_surf_vector = pg.Vector2(Config.INTERNAL_SURFACE_SIZE)
        x, y = Config.INTERNAL_SURFACE_SIZE[0] // 2 - Config.HALF_WIDTH, Config.INTERNAL_SURFACE_SIZE[1] // 2 - Config.HALF_HEIGHT
        self.internal_offset = pg.Vector2(x, y)
        ##############
        self._fps_font = pg.font.SysFont('arial', 30)  # Можна було б щось гарніше
        self._info_font = pg.font.SysFont('arial', 20)

    def bg(self):
        self._sc.fill('black')

    def world(self):
        if self.app.engine.preview:
            [self._sc.blit(obj.image, obj.rect) for obj in self.app.engine.parser.current_world]
            return
        self.internal_surf.fill((30, 30, 30))
        [self.internal_surf.blit(obj.image, obj.rect.topleft + self.internal_offset) for obj in self.app.engine.parser.current_world]
        scaled_surf = pg.transform.scale(self.internal_surf, self.internal_surf_vector * self.app.engine.parser.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=Config.CENTER)
        self._sc.blit(scaled_surf, scaled_rect)

    def tabs(self):
        self.app.engine.objects_list.draw()
        self.app.engine.editor.draw_on_screen()

    def info(self):
        obj_count = len(self.app.engine.parser.current_world)
        pos = pg.mouse.get_pos()
        zoom = f'{self.app.engine.parser.zoom_scale: .2f}'
        render = self._info_font.render(f'Total objects: {obj_count}  Mouse position: {pos}  Zoom coeff: {zoom}', True, 'white')
        x = Config.HALF_WIDTH - (render.get_size()[0] // 2)
        self._sc.blit(render, (x, Config.HEIGHT - 30))

    def fps(self):
        fps = self._fps_font.render(f'{self.app.clock.get_fps(): .1f}', True, Config.FPS_COLOR)
        self._sc.blit(fps, Config.FPS_POS)

    def all(self):
        self.bg()
        self.world()
        self.tabs()
        self.info()
        self.fps()
