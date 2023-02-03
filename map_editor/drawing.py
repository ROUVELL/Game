import pygame as pg
from config import Config


class Drawing:
    def __init__(self, engine):
        self._engine = engine
        self._sc = pg.display.get_surface()
        ##############
        self._info_font = pg.font.Font(Config.INFO_FONT, 8)
        self.grid_size = 32
        ##############
        self.draw_axis = not Config.DRAW_COORDINATE_AXIS
        self.draw_tiles_grid = Config.DRAW_TILE_GRID

    def _axis(self):
        x, y = self._engine.parser.origin
        w, h = Config.SCREEN
        pg.draw.line(self._sc, 'gray', (0, y), (w, y))
        pg.draw.line(self._sc, 'gray', (x, 0), (x, h))

    def _grid(self):
        w, h = Config.WIDTH, Config.HEIGHT
        origin = self._engine.parser.origin

        offset = pg.Vector2(
            x=origin.x - int(origin.x / self.grid_size) * self.grid_size,
            y=origin.y - int(origin.y / self.grid_size) * self.grid_size)

        [pg.draw.line(self._sc, (30, 30, 30), (dx, 0), (dx, h)) for dx in range(int(offset.x), w, self.grid_size)]
        [pg.draw.line(self._sc, (30, 30, 30), (0, dy), (w, dy)) for dy in range(int(offset.y), h, self.grid_size)]

    def _selected_objs_and_rect(self):
        for obj in self._engine.selected_objs:
            pg.draw.rect(self._sc, 'black', obj.rect, 1)
        rect = self._engine.selected_rect
        if self._engine.select_triger:
            surf = pg.Surface(rect.size)
            surf.set_alpha(30)
            surf.fill('lightgreen')
            self._sc.blit(surf, rect)
        if self._engine.select_triger or self._engine.selected_objs:
            pg.draw.rect(self._sc, 'skyblue', rect, 1)

    def _text(self, text, pos: tuple[int, int]):
        self._sc.blit(self._info_font.render(str(text), 0, 'white'), pos)

    def _engine_info(self):
        fps = f'{self._engine.app.clock.get_fps(): .1f}'
        auto_save = Config.AUTOSAVE
        preview = self._engine.preview
        text = f'Autosave: {auto_save}   Preview: {preview}   FPS: {fps}'
        pos = (Config.HALF_WIDTH - 80, 14)
        self._text(text, pos)
        color = 'red' if self._engine.parser.changed else 'green'
        pg.draw.rect(self._sc, color, (pos[0] - 15, pos[1], 6, 6))

    def _world_info(self):
        # К-сть об'єктів, позиція миші, поточний z індекс та тип
        obj_count = len(self._engine.parser.get_world())
        x, y = pg.math.Vector2(pg.mouse.get_pos()) - self._engine.parser.origin
        zindex = self._engine.objects_list.curr_zindex
        selected = self._engine.selected_rect.size if self._engine.select_triger else None

        text = f'Total objects: {obj_count}   Mouse position: {int(x), int(y)}   Selected: {selected}   Current z-index: {zindex}'
        pos = (Config.HALF_WIDTH - 210, Config.HEIGHT - 20)
        self._text(text, pos)

    def _obj_preview(self):
        obj = self._engine.objects_list.selected_obj
        if obj:
            img = obj.image.copy()
            img.set_alpha(180)
            rect = img.get_rect(center=pg.mouse.get_pos())
            self._sc.blit(img, rect)

    def _obj_info(self):
        if self._engine.select_triger:
            return
        # Показує інформацію про наведений мишею тайл
        x, y = pg.mouse.get_pos()
        # Беремо всі тайли на які навелись, по z індексу від верхніх до нижніх
        obj = self._engine.parser.get_collided_obj()
        origin = self._engine.parser.origin
        if obj:
            rect = obj.rect
            pg.draw.rect(self._sc, 'orange', rect, 1)
            self._text(int(rect.centery - origin.y), (rect.centerx - 5, rect.top - 8))
            self._text(int(rect.centerx - origin.x), (rect.left - 15, rect.centery - 5))
            self._text(rect.width, (rect.centerx - 5, rect.bottom + 2))
            self._text(rect.height, (rect.right + 2, rect.centery - 5))
            pg.draw.rect(self._sc, 'green', (x, y, 65, 47), 1)
            self._text(f'type: {obj.type}', (x + 5, y + 5))
            self._text(f'alpha: {obj.alpha}', (x + 5, y + 20))
            self._text(f'z-index: {obj.zindex}', (x + 5, y + 35))

    def world(self):
        if self.draw_tiles_grid: self._grid()
        for obj in self._engine.parser.get_world():
            self._sc.blit(obj.image, obj.rect)
            if Config.DRAW_TEXTURE_RECT: pg.draw.rect(self._sc, 'grey', obj.rect, 1)
        if Config.DRAW_SCREEN_CENTER: pg.draw.circle(self._sc, 'red', Config.CENTER, 3)
        if self.draw_axis: self._axis()
        self._selected_objs_and_rect()

    def info(self):
        self._engine_info()
        self._world_info()
        if self._engine.preview: return
        if self._engine.focus_on_world:
            self._obj_preview()
            self._obj_info()

    def tab(self):
        if not self._engine.preview:
            self._engine.objects_list.draw(self._sc)

    def all(self):
        self._sc.fill('black')
        self.world()
        self.info()
        self.tab()
