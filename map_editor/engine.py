import pygame as pg
from map_editor.parser import Parser
from map_editor.editor import ObjectsList, ObjectEditor
from config import Config


class Engine:
    def __init__(self, app):
        self.app = app
        self.parser = Parser(self)
        self.objects_list = ObjectsList(self)
        self.object_editor = ObjectEditor(self)
        ##########
        self.focus_on_world = self._check_focus()
        self.preview = False

    def _check_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    if not self.preview and (self.objects_list.selected_obj or self.object_editor.selected_obj):
                        self.objects_list.selected_obj = None
                        self.object_editor.selected_obj = None
                        continue
                    if Config.AUTO_SAVE: self.parser.save_world()
                    self.app.running = False
                elif event.key == pg.K_p: self.preview = not self.preview
                elif event.key == pg.K_s:
                    if pg.key.get_pressed()[pg.K_LCTRL]: self.parser.save_world()
                elif event.key == pg.K_RSHIFT: self.objects_list.curr_zindex += 1
                elif event.key == pg.K_RCTRL: self.objects_list.curr_zindex -= 1
                elif event.key == pg.K_g:
                    tile = self.parser.get_collided_rect()
                    if tile:
                        tile.type = 'sprite' if tile.type == 'texture' else 'texture'
            elif event.type == pg.MOUSEBUTTONUP and not self.preview:
                if event.button == 1:
                    if self.objects_list.selected_obj: self.objects_list.add_selected_to_world(event.pos)
                    elif self.focus_on_world: self.object_editor.select_obj()
                elif event.button == 3 and self.focus_on_world:
                    # Shift + RKM - видалити всі об'єкти
                    if pg.key.get_pressed()[pg.K_LSHIFT]: self.parser.delete_from_world(event.pos, True)
                    else: self.parser.delete_from_world(event.pos)
            elif event.type == pg.MOUSEWHEEL and self.objects_list.in_focus and not self.preview:
                self.objects_list.slide_list(event.y)

    def _check_focus(self):
        # True якщо не наведені не на одну з вкладок
        self.focus_on_world = not (self.objects_list.check_focus() or self.object_editor.check_focus())

    def _mouse_control(self):
        ox, oy = pg.mouse.get_rel()
        keys = pg.mouse.get_pressed()
        if keys[1]: self.parser.offset(ox * .5, oy * .5)

    def _keyboard_control(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LCTRL]: return

        if keys[pg.K_w]: self.parser.offset(0, 2)
        elif keys[pg.K_s]: self.parser.offset(0, -2)
        if keys[pg.K_a]: self.parser.offset(2, 0)
        elif keys[pg.K_d]: self.parser.offset(-2, 0)

    def update(self):
        self._check_focus()
        self._check_events()
        if self.focus_on_world:
            self._mouse_control()
            self._keyboard_control()
        if not self.preview:  # Оновлюємо якщо не наведені на світ
            self.objects_list.update()
            self.object_editor.update()
