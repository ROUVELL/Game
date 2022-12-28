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
        ##########
        self.focus_on_world = True

    def _normalize_mouse_pos(self, pos: tuple):
        return pos

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE: exit()
                if event.key == pg.K_s: self.parser.save_world()
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1: self.objects_list.add_selected_to_world(event.pos)
                elif event.button == 3:
                    # Shift + RKM - видалити всі об'єкти
                    if pg.key.get_pressed()[pg.K_LSHIFT]: self.parser.delete_from_world(event.pos, True)
                    else: self.parser.delete_from_world(event.pos)
            if event.type == pg.MOUSEWHEEL:
                if self.objects_list.in_focus: self.objects_list.slide_list(event.y)

    def check_focus_on_world(self):
        # True якщо не наведені не на одну з вкладок
        self.focus_on_world = not (self.objects_list.in_focus or self.editor.in_focus)

    def mouse_control(self):
        # Мишка не може бути наведена на два елементи одночасно тому використовую elif
        if self.objects_list.in_focus or self.objects_list.selected_obj is not None: self.objects_list.update()
        elif self.editor.in_focus: self.objects_list.update()

        ox, oy = pg.mouse.get_rel()
        keys = pg.mouse.get_pressed()
        if keys[1]:
            self.parser.offset(ox, oy)

    def update(self):
        self.check_events()
        self.objects_list.check_focus()
        self.editor.check_focus()
        self.check_focus_on_world()
        self.mouse_control()
