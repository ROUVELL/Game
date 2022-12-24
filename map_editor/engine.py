import pygame as pg
from parser import Parser
from editor import ObjectsList, Editor
from config import Config


class Engine:
    def __init__(self, app):
        self.app = app
        self.parser = Parser(self)
        self.objects_list = ObjectsList(self)
        self.editor = Editor(self)

    def check_events(self):
        [exit() for event in pg.event.get() if event.type == pg.KEYUP and event.key == pg.K_ESCAPE]

    def mouse_control(self):
        x, y = pg.mouse.get_pos()
        ox, oy = pg.mouse.get_rel()

        self.objects_list.check_focus(x, y)
        self.editor.check_focus(x, y)

        keys = pg.mouse.get_pressed()
        if keys[1]:
            self.parser.offset(ox, oy)


    def update(self):
        self.mouse_control()
        self.check_events()
        self.objects_list.update()
        self.editor.update()