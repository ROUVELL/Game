import pygame as pg
from config import Config


class Drawing:
    def __init__(self, engine):
        self._engine = engine
        self._sc = pg.display.get_surface()
        ##############
        self._info_font = pg.font.Font(Config.INFO_FONT, 8)
        # Поверхня для малювання сітки та її розмір
        self._grid_surf = pg.Surface(Config.SCREEN)
        self._grid_surf.set_colorkey('black')
        self._grid_surf.set_alpha(50)
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
        cols = Config.WIDTH // self.grid_size
        rows = Config.HEIGHT // self.grid_size
        origin = self._engine.parser.origin

        offset = pg.Vector2(
            x=origin.x - int(origin.x / self.grid_size) * self.grid_size,
            y=origin.y - int(origin.y / self.grid_size) * self.grid_size)

        self._grid_surf.fill('black')
        for col in range(cols + 1):
            x = offset.x + col * self.grid_size
            pg.draw.line(self._grid_surf, 'darkgrey', (x, 0), (x, Config.HEIGHT))

        for row in range(rows + 1):
            y = offset.y + row * self.grid_size
            pg.draw.line(self._grid_surf, 'darkgrey', (0, y), (Config.WIDTH, y))

        self._sc.blit(self._grid_surf, (0, 0))

    def _selected_rect(self):
        rect = self._engine.selected_rect
        surf = pg.Surface(rect.size)
        surf.set_alpha(20)
        surf.fill('lightgreen')
        self._sc.blit(surf, rect)

    def _text(self, text, pos: tuple[int | int]):
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
        type_ = self._engine.objects_list.curr_type
        selected = self._engine.selected_rect.size if self._engine.select_triger else None

        text = f'Total objects: {obj_count}   Mouse position: {int(x), int(y)}   Selected: {selected}   Current type: {type_}   Current z-index: {zindex}'
        pos = (Config.HALF_WIDTH - 210, Config.HEIGHT - 20)
        self._text(text, pos)

    def _obj_info(self):
        # Показує інформацію про наведений мишею тайл
        x, y = pg.mouse.get_pos()
        # Беремо всі тайли на які навелись, по z індексу від верхніх до нижніх
        obj = self._engine.parser.get_collided_obj()
        origin = self._engine.parser.origin
        if obj:
            rect = obj.rect
            pg.draw.rect(self._sc, 'orange', rect, 1)
            self._text(rect.centery - origin.y, (rect.centerx - 5, rect.top - 8))
            self._text(rect.centerx - origin.x, (rect.left - 10, rect.centery - 5))
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
        if self._engine.select_triger: self._selected_rect()

    def info(self):
        self._engine_info()
        self._world_info()
        if self._engine.preview: return
        if self._engine.focus_on_world:
            obj = self._engine.objects_list.selected_obj
            if obj:
                img = obj.image.copy()
                img.set_alpha(180)
                w, h = img.get_size()
                x, y = pg.mouse.get_pos()
                pos = (x - w // 2, y - h // 2)
                self._sc.blit(img, pos)
            self._obj_info()

    def tab(self):
        if not self._engine.preview:
            self._engine.objects_list.draw(self._sc)

    def all(self):
        self._sc.fill('black')
        self.world()
        self.info()
        self.tab()
