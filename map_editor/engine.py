import pygame as pg
from map_editor.drawing import Drawing
from map_editor.parser import Parser
from map_editor.objects_tab import ObjectsTab
from config import Config


class Engine:
    def __init__(self, app):
        self.app = app
        self.draw = Drawing(self)
        self.parser = Parser(self)
        self.objects_list = ObjectsTab(self)
        ##########
        self.start_point = None
        self.selected_rect = pg.Rect(0, 0, 0, 0)
        ##########
        self.focus_on_world = False
        self.preview = False
        self.select_triger = False
        self.selected_objs = []
        ##########
        if Config.AUTOSAVE: pg.time.set_timer(pg.USEREVENT, int(Config.AUTOSAVE_DELEY * 1000), -1)

    def _key_event(self, event: pg.event.Event):
        # ESC - clear selected objs / clear seleced obj. in tab / exit
        # o - move to origin
        # p - preview
        # x - draw origin axis
        # z - draw tiles grid
        # DELETE - remove selected objs. from world
        # LCTRL + s - save world
        # LCTRL + r - restore world
        # RSHIFT and RCTRL - curr index +- 1
        match event.key:
            case pg.K_ESCAPE:
                if not self.preview:
                    if self.objects_list.selected_obj:
                        self.objects_list.selected_obj = None
                        return
                    if self.selected_objs:
                        self.selected_objs.clear()
                        return
                if Config.AUTOSAVE_ON_EXIT: self.parser.save_world()
                self.app.running = False
            case pg.K_o:
                self.parser.origin = pg.Vector2(Config.CENTER)
            case pg.K_p:
                self.preview = not self.preview
            case pg.K_x:
                self.draw.draw_axis = not self.draw.draw_axis
            case pg.K_z:
                self.draw.draw_tiles_grid = not self.draw.draw_tiles_grid
            case pg.K_s:
                if pg.key.get_pressed()[pg.K_LCTRL]: self.parser.save_world()
            case pg.K_r:
                if pg.key.get_pressed()[pg.K_LCTRL]: self.parser.restore_world()
            case pg.K_a:
                if not self.focus_on_world: self.objects_list.rotate_group(-1)
            case pg.K_d:
                if not self.focus_on_world: self.objects_list.rotate_group(1)
            case pg.K_DELETE:
                [obj.kill() for obj in self.selected_objs]
                self.selected_objs.clear()
            case pg.K_RSHIFT:
                self.objects_list.curr_zindex += 1
            case pg.K_RCTRL:
                self.objects_list.curr_zindex -= 1

    def _mouse_events(self, event: pg.event.Event):
        # LKM - add selected obj to world / select obj from world
        # RKM - delete one collided obj
        # LSHIFT + RKM - delete all collided objs
        if event.type == pg.MOUSEBUTTONUP and self.focus_on_world:
            if event.button == 1:
                if self.objects_list.selected_obj: self.objects_list.add_selected_to_world(event.pos)
                self.select_triger = False
            elif event.button == 3:
                if pg.key.get_pressed()[pg.K_LSHIFT]:
                    self.parser.delete_collided_obj(event.pos, all_=True)
                else:
                    self.parser.delete_collided_obj(event.pos)

        elif event.type == pg.MOUSEWHEEL:
            if self.focus_on_world:
                size = self.draw.grid_size
                size = size // 2 if event.y < 0 else size * 2
                self.draw.grid_size = max(min(size, 256), 16)
            else:
                self.objects_list.slide_list(event.y)

    def _check_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYUP:
                self._key_event(event)
            elif event.type in [pg.MOUSEBUTTONUP, pg.MOUSEWHEEL] and not self.preview:
                self._mouse_events(event)
            elif event.type == pg.USEREVENT:
                self.parser.save_world()

    def _check_focus(self):
        # True якщо не наведені не на одну з вкладок
        self.focus_on_world = not self.objects_list.check_focus()

    def _select(self):
        pos = pg.Vector2(pg.mouse.get_pos())
        if not self.select_triger:
            self.select_triger = True
            self.start_point = pos
        x, y = self.start_point
        w, h = pos - self.start_point
        if w >= 0 and h >= 0:
            self.selected_rect = pg.Rect((x, y), (w, h))
        elif w < 0 and h < 0:
            self.selected_rect = pg.Rect((x + w, y + h), (-w, -h))
        elif w < 0 <= h:
            self.selected_rect = pg.Rect((x + w, y), (-w, h))
        elif h < 0 <= w:
            self.selected_rect = pg.Rect((x, y + h), (w, -h))
        self.selected_objs.clear()
        for obj in self.parser.get_world():
            if self.selected_rect.contains(obj.rect):
                self.selected_objs.append(obj)

    def _mouse_control(self):
        offset = pg.Vector2(pg.mouse.get_rel())
        keys = pg.mouse.get_pressed()
        if keys[1]:
            self.parser.offset(offset * .5)
            self.selected_rect.move_ip(offset * .5)
        if keys[0]:
            if not self.objects_list.selected_obj:
                if not self.select_triger and self.selected_rect.collidepoint(pg.mouse.get_pos()):
                    [obj.rect.move_ip(offset * .5) for obj in self.selected_objs]
                    self.selected_rect.move_ip(offset * .5)
                else:
                    self._select()
            else:
                self.select_triger = False

    def _keyboard_control(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LCTRL]: return

        offset = pg.Vector2()
        if keys[pg.K_w]:
            offset.y = -2
        elif keys[pg.K_s]:
            offset.y = 2
        if keys[pg.K_a]:
            offset.x = -2
        elif keys[pg.K_d]:
            offset.x = 2

        if self.selected_objs:
            [obj.rect.move_ip(offset) for obj in self.selected_objs]
            self.selected_rect.move_ip(offset)
        else: self.parser.offset(-offset)

    def update_and_draw(self):
        self._check_focus()
        self._check_events()
        if self.focus_on_world:
            self._mouse_control()
            self._keyboard_control()
        if not self.preview:
            self.objects_list.update()

        self.draw.all()
