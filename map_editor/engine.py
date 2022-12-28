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
        self.focus_on_world = self._check_focus()

    def _check_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    if Config.AUTO_SAVE: self.parser.save_world()
                    exit()
                if event.key == pg.K_s: self.parser.save_world()
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1: self.objects_list.add_selected_to_world(event.pos)
                if event.button == 3:
                    # Shift + RKM - видалити всі об'єкти
                    if pg.key.get_pressed()[pg.K_LSHIFT]: self.parser.delete_from_world(event.pos, True)
                    else: self.parser.delete_from_world(event.pos)
            if event.type == pg.MOUSEWHEEL and self.objects_list.in_focus: self.objects_list.slide_list(event.y)

    def _check_focus(self):
        # True якщо не наведені не на одну з вкладок
        self.focus_on_world = not (self.objects_list.check_focus() or self.editor.check_focus())
        return self.focus_on_world

    def _mouse_control(self):
        ox, oy = pg.mouse.get_rel()
        keys = pg.mouse.get_pressed()
        if keys[1]: self.parser.offset(ox, oy)

    def update(self):
        self._check_events()
        self._mouse_control()
        if not self._check_focus():  # Оновлюємо якщо не наведені на світ
            self.objects_list.update()
            self.editor.update()
