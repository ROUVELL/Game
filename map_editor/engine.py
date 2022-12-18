import pygame as pg
from config import Config


class Engine:
    def __init__(self, editor):
        self.editor = editor

    def mouse_control(self):
        ox, oy = pg.mouse.get_rel()
        keys = pg.mouse.get_pressed()
        if keys[1]:
            self.editor.parser.offset(ox, oy)

    def update(self):
        self.mouse_control()