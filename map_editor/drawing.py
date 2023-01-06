import pygame as pg
from config import Config


class Drawing:
    def __init__(self, engine):
        self.engine = engine
        self._sc = pg.display.get_surface()
        ##############
        self._fps_font = pg.font.Font(Config.INFO_FONT, 16)
        self._info_font = pg.font.Font(Config.INFO_FONT, 8)

    def bg(self):
        self._sc.fill('black')

    def world(self):
        for obj in self.engine.parser.current_world:
            self._sc.blit(obj.image, obj.rect)
            if Config.DRAW_TEXTURE_RECT: pg.draw.rect(self._sc, 'grey', obj.rect, 1)
        if Config.DRAW_SCREEN_CENTER: pg.draw.circle(self._sc, 'red', Config.CENTER, 3)

    def tab(self):
        if not self.engine.preview:
            self.engine.objects_list.draw(self._sc)

    def _text(self, text, pos: tuple):
        self._sc.blit(self._info_font.render(str(text), 0, 'white'), pos)

    def _world_info(self):
        # К-сть об'єктів, позиція миші та поточний z індекс
        obj_count = len(self.engine.parser.current_world)
        x, y = pg.mouse.get_pos()
        zindex = self.engine.objects_list.curr_zindex
        type_ = self.engine.objects_list.curr_type
        text = f'Total objects: {obj_count}  Mouse position: {x, y}  Current type: {type_}  Current z-index: {zindex}'
        pos = (Config.HALF_WIDTH - 164, Config.HEIGHT - 30)
        self._text(text, pos)

    def _tile_info(self):
        # Показує інформацію про наведений мишею тайл
        x, y = pg.mouse.get_pos()
        # Беремо всі тайли на які навелись, по z індексу від верхніх до нижніх
        obj = self.engine.parser.get_collided_rect()
        if obj:
            rect = obj.rect
            pg.draw.rect(self._sc, 'grey', rect, 1)
            self._text(rect.centery, (rect.centerx - 5, rect.top - 8))
            self._text(rect.centerx, (rect.left - 10, rect.centery - 5))
            self._text(rect.width, (rect.centerx - 5, rect.bottom + 2))
            self._text(rect.height, (rect.right + 2, rect.centery - 5))
            pg.draw.rect(self._sc, 'green', (x, y, 65, 47), 1)
            self._text(f'type: {obj.type}', (x + 5, y + 5))
            self._text(f'alpha: {obj.alpha}', (x + 5, y + 20))
            self._text(f'z-index: {obj.zindex}', (x + 5, y + 35))

    def info(self):
        self._world_info()
        if self.engine.preview: return
        if self.engine.focus_on_world:
            obj = self.engine.objects_list.selected_obj
            if obj:
                img = obj.image.copy()
                img.set_alpha(180)
                w, h = img.get_size()
                x, y = pg.mouse.get_pos()
                pos = (x - w // 2, y - h // 2)
                self._sc.blit(img, pos)
            self._tile_info()

    def fps(self):
        self._sc.blit(self._fps_font.render(f'{self.engine.app.clock.get_fps(): .1f}', 0, Config.FPS_COLOR), Config.FPS_POS)

    def all(self):
        self.bg()
        self.world()
        self.info()
        self.tab()
        self.fps()
