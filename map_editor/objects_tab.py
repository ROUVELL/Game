import pygame as pg
from config import Config

import json


class _ObjectsGroupItem:
    def __init__(self, img: pg.Surface, name: str):
        self.name = name
        self.image = img.convert_alpha()


class _ObjectsGroup:
    def __init__(self, name: str, pos: tuple[int, int], obj: _ObjectsGroupItem):
        self.name = name
        ##########
        self.rect = pg.Rect(0, 0, Config.OBJECTS_LIST_SIZE[0], Config.OBJECTS_LIST_SIZE[0])
        self.rect.center = pos
        ##########
        self.curr_obj = obj
        self._items = []
        self._index = 0
        self._in_focus = False
        if obj:
            self.add_objs(obj)

    def add_objs(self, objs: list[_ObjectsGroupItem, ...] | _ObjectsGroupItem):
        # Додає один або декілька об'єктів до групи
        assert isinstance(objs, (list, _ObjectsGroupItem))
        if isinstance(objs, list):
            [self._items.append(obj) for obj in objs]
        else: self._items.append(objs)

    def draw(self, sc: pg.Surface):
        img = self.curr_obj.image
        rect = img.get_rect(center=self.rect.center)
        if self._in_focus:
            pg.draw.rect(sc, 'red', self.rect, 1)
        sc.blit(img, rect)

    def update(self):
        self._in_focus = False
        self.curr_obj = self._items[self._index]
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self._in_focus = True


class ObjectsTab:
    def __init__(self, engine):
        self._parser = engine.parser
        self._sc = pg.Surface(Config.OBJECTS_LIST_SIZE)
        self._sc.set_alpha(200)
        self._rect = self._sc.get_rect(topleft=Config.OBJECTS_LIST_POS)
        #############
        config = open(Config.STATIC_CONFIG, encoding='utf-8')
        self._static_config = json.load(config)
        config.close()
        #############
        self.in_focus = False  # Чи наведена мишка
        self.selected_obj = None  # !!! Tут лежить об'єкт !!!
        self._items = dict()  # Список груп
        self.curr_zindex = 1
        self._get_items()

    def _get_items(self):
        # Початкові координати та зміщення по вертикалі
        x = y = self._rect.width // 2
        offset = self._rect.width + 5
        # Проходимо циклом по всіх статичних фотках
        for name, img in self._parser.cached_images.items():
            # Буремо назву групи, якщо такої ще не існує - створюємо
            group_name = self._static_config[name]['group']
            if group_name not in self._items:
                self._items[group_name] = _ObjectsGroup(name=group_name, pos=(x, y), obj=_ObjectsGroupItem(img=img, name=name))
                y += offset

            self._items[group_name].add_objs(_ObjectsGroupItem(img=img, name=name))
        self._items = dict(sorted(self._items.items(), key=lambda x: x[0]))

    def slide_list(self, offset: int | float):
        # Прокручеємо список якщо наведені на нього мишкою
        [group.rect.move_ip(0, offset * Config.SLIDE_SENSETIVITY) for group in self._items.values()]

    def _select_obj(self):
        # Беремо об'єкт зі списка
        x, y = pg.mouse.get_pos()
        for group in self._items.values():
            if group.rect.collidepoint(x, y):
                self.selected_obj = group.curr_obj
                return

    def add_selected_to_world(self, pos: tuple[int, int]):
        # Додаємо вибраний об'єкт до світу
        obj = self.selected_obj
        parr = self._static_config[obj.name]
        self._parser.add_to_world(
            type=parr['type'],
            name=obj.name,
            pos=pos,
            alpha=parr['alpha'],
            zindex=self.curr_zindex
        )

    def _keyboard_control(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.slide_list(.2)
        elif keys[pg.K_s]:
            self.slide_list(-.2)

    def check_focus(self) -> bool:
        self.in_focus = self._rect.collidepoint(*pg.mouse.get_pos())
        return self.in_focus

    def draw(self, sc: pg.Surface):
        self._sc.fill((20, 0, 0))
        [group.draw(sc) for group in self._items.values()]

    def update(self):
        if self.in_focus:
            self._keyboard_control()
            [group.update() for group in self._items.values()]
            keys = pg.mouse.get_pressed()
            if keys[0]: self._select_obj()
