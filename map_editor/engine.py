import pygame as pg
from parser import Parser
from config import Config


class Engine:
    def __init__(self, editor):
        self.editor = editor
        self.world = Parser(self)
        self.select_object = None

    def mouse_control(self):
        ox, oy = pg.mouse.get_rel()
        keys = pg.mouse.get_pressed()
        if keys[0]:
            self.select_object = self.world.select_element(*pg.mouse.get_pos())
        if keys[1]:
            self.world.offset(ox, oy)

    def update(self):
        self.mouse_control()