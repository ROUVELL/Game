import pygame as pg
from map_editor.drawing import Drawing
from map_editor.parser import Parser
from map_editor.object_list import ObjectsList
from config import Config


class Engine:
    def __init__(self, app):
        self.app = app
        self.draw = Drawing(self)
        self.parser = Parser(self)
        self.objects_list = ObjectsList(self)
        ##########
        # TODO: Виділення мишкою області на світі як на робочому столі віндовс
        ##########
        self.start_point = None
        self.selected_rect = None
        ##########
        self.focus_on_world = False
        self.preview = False
        self.select_triger = False
        ##########
        if Config.AUTOSAVE: pg.time.set_timer(pg.USEREVENT, int(Config.AUTOSAVE_DELEY * 1000), -1)

    def _key_event(self, event: pg.event.Event):
        # ESC - clear seleced obj. in tabs / exit
        # p - preview
        # g - change type of collided obj (texture/sprite)
        # x - draw origin axis
        # z - draw tiles grid
        # LCTRL + s - save world
        # LCTRL + r - restore world
        # RSHIFT and RCTRL - curr index +- 1
        # TAB - change current type between 'rexture' and 'sprite'
        match event.key:
            case pg.K_ESCAPE:
                if not self.preview and self.objects_list.selected_obj:
                    self.objects_list.selected_obj = None
                    return
                if Config.AUTOSAVE_ON_EXIT: self.parser.save_world()
                self.app.running = False
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
            case pg.K_RSHIFT:
                self.objects_list.curr_zindex += 1
            case pg.K_RCTRL:
                self.objects_list.curr_zindex -= 1
            case pg.K_TAB:
                self.objects_list.curr_type = 'sprite' if self.objects_list.curr_type == 'texture' else 'texture'
            case pg.K_g:
                if self.preview: return
                tile = self.parser.get_collided_obj()
                if tile:
                    tile.type = 'sprite' if tile.type == 'texture' else 'texture'

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

    def _mouse_control(self):
        ox, oy = pg.mouse.get_rel()
        keys = pg.mouse.get_pressed()
        if keys[1]: self.parser.offset(ox * .5, oy * .5)
        if keys[0]:
            if not self.objects_list.selected_obj:
                self._select()
            else: self.select_triger = False


    def _keyboard_control(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LCTRL]: return

        if keys[pg.K_w]:
            self.parser.offset(0, 2)
        elif keys[pg.K_s]:
            self.parser.offset(0, -2)
        if keys[pg.K_a]:
            self.parser.offset(2, 0)
        elif keys[pg.K_d]:
            self.parser.offset(-2, 0)

    def update_and_draw(self):
        self._check_focus()
        self._check_events()
        if self.focus_on_world:
            self._mouse_control()
            self._keyboard_control()
        if not self.preview:
            self.objects_list.update()

        self.draw.all()
