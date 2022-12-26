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
        for event in pg.event.get():
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE: exit()
                if event.key == pg.K_s: self.parser.save_world()
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if self.objects_list.selected_obj is not None: self.objects_list.add_selected_to_world(event.pos)
            if event.type == pg.MOUSEWHEEL:
                if self.objects_list.in_focus: self.objects_list.slide_list(event.y)
                else: self.parser.scale_coeff += event.y

    def mouse_control(self):
        # Мишка не може бути наведена на два елементи одночасно тому використовую elif
        if self.objects_list.in_focus or self.objects_list.selected_obj is not None:
            self.objects_list.update()
        elif self.editor.in_focus:
            self.objects_list.update()

        ox, oy = pg.mouse.get_rel()
        keys = pg.mouse.get_pressed()
        if keys[1]:
            self.parser.offset(ox, oy)

    def update(self):
        self.check_events()
        self.objects_list.check_focus()
        self.editor.check_focus()
        self.mouse_control()
