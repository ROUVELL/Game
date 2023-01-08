import pygame as pg
from config import Config


class _ObjectListItem:
    def __init__(self, img: pg.Surface, name: str, pos: tuple):
        self.name = name
        self.image = img.convert_alpha()
        self.rect = img.get_rect(center=pos)


class ObjectsList:
    def __init__(self, engine):
        self._parser = engine.parser
        self._sc = pg.Surface(Config.OBJECTS_LIST_SIZE)
        self._sc.set_alpha(200)
        self._rect = self._sc.get_rect(topleft=Config.OBJECTS_LIST_POS)
        #############
        self.in_focus = False  # Чи наведена мишка
        self.selected_obj = None  # !!! Tут лежить об'єкт !!!
        self._items = set()
        self.curr_zindex = 1
        self.curr_type = 'texture'
        self._get_items()

    def _get_items(self):
        x = self._rect.width // 2
        offset = 20
        for name, img in self._parser.cached_images.items():
            dh = img.get_height() // 2
            offset += dh
            self._items.add(_ObjectListItem(img, name, (x, offset)))
            offset += dh + 10

    def slide_list(self, offset: int | float):
        # Прокручеємо список якщо наведені на нього мишкою
        [obj.rect.move_ip(0, offset * Config.SLIDE_SENSETIVITY) for obj in self._items]

    def _select_obj(self):
        # Беремо об'єкт зі списка
        x, y = pg.mouse.get_pos()
        for obj in self._items:
            if obj.rect.collidepoint(x, y):
                self.selected_obj = obj
                return

    def add_selected_to_world(self, pos: tuple[int | int]):
        # Додаємо вибраний об'єкт до світу
        obj = self.selected_obj
        self._parser.add_to_world(
            image=obj.image,
            type=self.curr_type,
            name=obj.name,
            pos=pos,
            alpha=True,
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

    def draw(self, sc):
        self._sc.fill('black')
        [self._sc.blit(obj.image, obj.rect) for obj in self._items]
        if self.selected_obj:
            pg.draw.rect(self._sc, 'red', self.selected_obj.rect.inflate(10, 10), 1)
        sc.blit(self._sc, self._rect)
        if self.in_focus:
            pg.draw.rect(sc, 'green', self._rect, 1, 2)

    def update(self):
        if self.in_focus:
            self._keyboard_control()
            keys = pg.mouse.get_pressed()
            if keys[0]: self._select_obj()
