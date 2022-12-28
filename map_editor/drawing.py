import pygame as pg
from config import Config


class Drawing:
    def __init__(self, app):
        self.app = app
        self._sc = app.sc
        ##############
        self._fps_font = pg.font.SysFont('arial', 30)  # Можна було б щось гарніше
        self._info_font = pg.font.SysFont('arial', 20)

    def bg(self):
        self._sc.fill('black')

    def world(self):
        for obj in self.app.engine.parser.current_world:
            self._sc.blit(obj.image, obj.rect)
            if Config.DRAW_TEXTURE_RECT: pg.draw.rect(self._sc, 'grey', obj.rect, 1)

    def tabs(self):
        self.app.engine.objects_list.draw()
        self.app.engine.editor.draw_on_screen()

    def _world_info(self):
        # К-сть об'єктів та позиція миші
        obj_count = len(self.app.engine.parser.current_world)
        x, y = pg.mouse.get_pos()
        render = self._info_font.render(f'Total objects: {obj_count}  Mouse position: {x, y}', True, 'white')
        dx = Config.HALF_WIDTH - (render.get_size()[0] // 2)
        self._sc.blit(render, (dx, Config.HEIGHT - 30))

    def _tile_info(self):
        # Показує інформацію про наведений мишею тайл
        x, y = pg.mouse.get_pos()
        # Беремо всі тайли на які навелись, по z індексу від верхніх до нижніх
        tiles = [obj for obj in self.app.engine.parser.current_world[::-1] if obj.rect.collidepoint(x, y)]
        if tiles:
            pg.draw.rect(self._sc, 'green', (x, y, 200, 170), 1)
            tile = tiles[0]
            self._sc.blits((
                (self._info_font.render(tile.name.partition('.')[0], True, 'darkgrey'), (x + 10, y + 15)),
                (self._info_font.render(f'size: {tile.rect.size}', True, 'white'), (x + 10, y + 45)),
                (self._info_font.render(f'pos: {tile.rect.center}', True, 'white'), (x + 10, y + 75)),
                (self._info_font.render(f'alpha: {tile.alpha}', True, 'white'), (x + 10, y + 105)),
                (self._info_font.render(f'z-index: {tile.zindex}', True, 'white'), (x + 10, y + 135))), doreturn=False)

    def info(self):
        self._world_info()
        if self.app.engine.focus_on_world: self._tile_info()
        # TODO: Квадрат куда поставиться вибраний тайл

    def fps(self):
        self._sc.blit(self._fps_font.render(f'{self.app.clock.get_fps(): .1f}', True, Config.FPS_COLOR), Config.FPS_POS)

    def all(self):
        self.bg()
        self.world()
        self.info()
        self.tabs()
        self.fps()
