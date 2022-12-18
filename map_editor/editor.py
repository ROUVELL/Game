import pygame as pg
from config import Config


class Tab:
    def __init__(self, size: tuple, pos: tuple):
        self.tab = pg.Surface(size)
        self.tab.set_alpha(100)
        self.tab_rect = self.tab.get_rect(topleft=pos)

    def check_click(self, pos: tuple) -> bool:
        return True if self.tab_rect.collidepoint(*pos) else False

    def draw(self):
        self.editor.app.sc.blit(self.tab, self.tab_rect)


class EditingTab(Tab):
    def __init__(self, editor):
        super().__init__(Config.EDITING_TAB_SIZE, Config.EDITING_TAB_POS)
        self.editor = editor
        self.object = None

    def click(self, pos: tuple) -> bool:
        if not self.object:
            return False
        return self.check_click(pos)


class ObjectsList(Tab):
    def __init__(self, editor):
        super().__init__(Config.OBJECTS_LIST_SIZE, Config.OBJECTS_LIST_POS)
        self.editor = editor
        self.objects = set()
        self.images = dict()

    def init(self):
        self.load_objects_and_images()

    def load_objects_and_images(self):
        self.objects = self.editor.app.engine.world.current_world
        self.images = self.editor.app.engine.world.cached_images

    def click(self, pos: tuple) -> bool:
        return self.check_click(pos)


class Editor:
    def __init__(self, app):
        self.app = app
        self.editing_tab = EditingTab(self)
        self.objects_list = ObjectsList(self)
        self.editing_object = None

    def init(self):
        self.objects_list.init()

    def update(self):
        self.editing_tab.object = self.editing_object

    def draw(self):
        self.objects_list.draw()
        if self.editing_object:
            self.editing_tab.draw()