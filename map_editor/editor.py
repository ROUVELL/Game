import pygame as pg
from config import Config


class __Tab:
    def __init__(self, engine, size: tuple, pos: tuple):
        self._engine = engine
        self._sc = pg.Surface(size)
        self._sc.set_alpha(200)
        self._rect = self._sc.get_rect(topleft=pos)
        self.in_focus = False  # Чи наведена мишка

    def check_focus(self):
        self.in_focus = self._rect.collidepoint(*pg.mouse.get_pos())

    def draw_on_screen(self):
        self._engine.app.sc.blit(self._sc, self._rect)
        # if self.in_focus:
        #     pg.draw.rect(self._engine.app.sc, 'green', self._rect, 1, 10)


class ObjectsList(__Tab):
    def __init__(self, engine):
        super().__init__(engine, Config.OBJECTS_LIST_SIZE, Config.OBJECTS_LIST_POS)
        self.selected_obj = None
        self._get_imgs_and_rects()

    def _get_imgs_and_rects(self):
        self._original_imgs = self._engine.parser.cached_images
        self.imgs_list = [pg.transform.scale2x(img) for img in self._original_imgs.values()]
        self.rects_list = [img.get_rect(center=(Config.OBJECTS_LIST_SIZE[0] // 2, i * 96 + 96)) for i, img in enumerate(self.imgs_list)]

    def slide_list(self, offset: int):
        if self.in_focus:
            [rect.move_ip(0, offset * Config.SLIDE_SENSETIVITY) for rect in self.rects_list]

    def _select_obj(self):
        x, y = pg.mouse.get_pos()
        for i, rect in enumerate(self.rects_list):
            if rect.collidepoint(x, y):
                return i

    def add_selected_to_world(self, pos):
        if not (self.in_focus or self._engine.editor.in_focus):
            img = self.imgs_list[self.selected_obj]
            size = img.get_size()
            self._engine.parser.add_to_world(
                img=img,
                size=size,
                pos=pos,
                alpha=True,
                zindex=0)

    def mouse_control(self):
        keys = pg.mouse.get_pressed()
        if keys[0]:
            if self.in_focus:  # Якщо ми навелись мишою то дивимось що ми вибрали
                self.selected_obj = self._select_obj()

    def draw(self):
        self._sc.fill('black')
        x = Config.OBJECTS_LIST_SIZE[0] // 2
        for i, img in enumerate(self.imgs_list):
            self._sc.blit(img, self.rects_list[i])
        if self.selected_obj is not None:
            pg.draw.rect(self._sc, 'red', self.rects_list[self.selected_obj].inflate(10, 10), 2)

        self.draw_on_screen()


    def update(self):
        self.mouse_control()


class Editor(__Tab):
    def __init__(self, engine):
        super().__init__(engine, Config.EDITING_TAB_SIZE, Config.EDITING_TAB_POS)

    def update(self):
        pass
