import pygame as pg
from config import Config


class __Tab:
    def __init__(self, engine, size: tuple, pos: tuple):
        self._engine = engine
        self._sc = pg.Surface(size)
        self._sc.set_alpha(120)
        self._rect = self._sc.get_rect(topleft=pos)
        self.in_focus = False  # Чи наведена мишка

    def check_focus(self, x: int, y: int):
        self.in_focus = self._rect.collidepoint(x, y)

    def draw_on_screen(self):
        self._engine.app.sc.blit(self._sc, self._rect)
        if self.in_focus:
            pg.draw.rect(self._engine.app.sc, 'green', self._rect, 1, 10)


class ObjectsList(__Tab):
    def __init__(self, engine):
        super().__init__(engine, Config.OBJECTS_LIST_SIZE, Config.OBJECTS_LIST_POS)


    def update(self):
        pass


class Editor(__Tab):
    def __init__(self, engine):
        super().__init__(engine, Config.EDITING_TAB_SIZE, Config.EDITING_TAB_POS)

    def update(self):
        pass
