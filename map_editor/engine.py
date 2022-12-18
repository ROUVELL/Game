import pygame as pg
from parser import Parser
from editor import Editor
from config import Config


class Engine:
    def __init__(self, app):
        self.world = Parser(self)
        self.editor = Editor(app)
        self.selected_object = None

    def init(self):
        self.editor.init()

    def mouse_control(self):
        ox, oy = pg.mouse.get_rel()
        keys = pg.mouse.get_pressed()
        if keys[0]:
            pos = pg.mouse.get_pos()
            if not self.editor.editing_tab.click(pos) and not self.editor.objects_list.click(pos):
                self.selected_object = self.editor.editing_object = self.world.select_element(pos)
        if keys[1]:
            self.world.offset(ox, oy)

    def update(self):
        self.mouse_control()
        self.editor.editing_object = self.selected_object
        self.editor.update()