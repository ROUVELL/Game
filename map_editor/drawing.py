import pygame as pg
from config import Config


class Drawing:
    def __init__(self, app):
        self.app = app
        self._sc = app.sc
        ##############
        self._fps_font = pg.font.Font(Config.INFO_FONT, 16)  # Можна було б щось гарніше
        self._info_font = pg.font.Font(Config.INFO_FONT, 8)
        ##############
        self.draw_size_info = Config.DRAW_OBJ_RECT
        self.draw_obj_info = Config.DRAW_OBJ_INFO

    def bg(self):
        self._sc.fill('black')

    def world(self):
        for obj in self.app.engine.parser.current_world:
            self._sc.blit(obj.image, obj.rect)
            if Config.DRAW_TEXTURE_RECT: pg.draw.rect(self._sc, 'grey', obj.rect, 1)
        if Config.DRAW_SCREEN_CENTER: pg.draw.circle(self._sc, 'red', Config.CENTER, 3)

    def tabs(self):
        self.app.engine.objects_list.draw()
        self.app.engine.editor.draw()

    def _world_info(self):
        # К-сть об'єктів та позиція миші
        obj_count = len(self.app.engine.parser.current_world)
        x, y = pg.mouse.get_pos()
        render = self._info_font.render(f'Total objects: {obj_count}  Mouse position: {x, y}', 0, 'white')
        dx = Config.HALF_WIDTH - (render.get_size()[0] // 2)
        self._sc.blit(render, (dx, Config.HEIGHT - 30))

    def _tile_info(self):
        # Показує інформацію про наведений мишею тайл
        x, y = pg.mouse.get_pos()
        # Беремо всі тайли на які навелись, по z індексу від верхніх до нижніх
        tiles = [obj for obj in self.app.engine.parser.current_world[::-1] if obj.rect.collidepoint(x, y)]
        if tiles:
            tile = tiles[0]
            rect = tile.rect
            if self.draw_size_info:
                pg.draw.rect(self._sc, 'grey', rect, 1)
                self._sc.blit(self._info_font.render(f'{rect.centery}', 0, 'white'), (rect.centerx - 5, rect.top - 8))
                self._sc.blit(self._info_font.render(f'{rect.centerx}', 0, 'white'), (rect.left - 10, rect.centery - 5))
                self._sc.blit(self._info_font.render(f'{rect.width}', 0, 'white'), (rect.centerx - 5, rect.bottom + 2))
                self._sc.blit(self._info_font.render(f'{rect.height}', 0, 'white'), (rect.right + 2, rect.centery - 5))
            if self.draw_obj_info:
                pg.draw.rect(self._sc, 'green', (x, y, 65, 32), 1)
                self._sc.blit(self._info_font.render(f'alpha: {tile.alpha}', 0, 'white'), (x + 10, y + 5))
                self._sc.blit(self._info_font.render(f'z-index: {tile.zindex}', 0, 'white'), (x + 10, y + 20))

    def info(self):
        self._world_info()
        if self.app.engine.focus_on_world:
            obj = self.app.engine.objects_list.selected_obj
            if obj:
                img = obj.image.copy()
                img.set_alpha(180)
                w, h = img.get_size()
                x, y = pg.mouse.get_pos()
                pos = (x - w // 2, y - h // 2)
                self._sc.blit(img, pos)
            self._tile_info()

    def fps(self):
        self._sc.blit(self._fps_font.render(f'{self.app.clock.get_fps(): .1f}', 0, Config.FPS_COLOR), Config.FPS_POS)

    def all(self):
        self.bg()
        self.world()
        self.info()
        self.tabs()
        self.fps()
