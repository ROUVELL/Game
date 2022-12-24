import pygame as pg
from parser import Parser
from editor import Editor
from config import Config


class Engine:
    def __init__(self, app):
        self.app = app
        self.current_world = Parser(self)
        self.editor = Editor(self)

    def mouse_control(self):
        ox, oy = pg.mouse.get_rel()
        keys = pg.mouse.get_pressed()
        if keys[1]:
            self.current_world.offset(ox, oy)

    def update(self):
        self.mouse_control()
        self.editor.update()