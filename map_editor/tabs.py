import pygame as pg
from config import Config


class __Tab:
    def __init__(self, engine, size: tuple, pos: tuple):
        self._engine = engine
        self._sc = pg.Surface(size)
        self._sc.set_alpha(200)
        self._rect = self._sc.get_rect(topleft=pos)
        ###############
        self.in_focus = False  # Чи наведена мишка

    def check_focus(self) -> bool:
        self.in_focus = self._rect.collidepoint(*pg.mouse.get_pos())
        return self.in_focus

    def _draw_on_screen(self):
        self._engine.app.sc.blit(self._sc, self._rect)
        # if self.in_focus:
        #     pg.draw.rect(self._engine.app.sc, 'green', self._rect, 1, 10)


class _ObjectListItem:
    def __init__(self, img: pg.Surface, name: str, pos: tuple):
        self.name = name
        self.image = img.convert_alpha()
        self.rect = img.get_rect(center=pos)


class ObjectsList(__Tab):
    def __init__(self, engine):
        super().__init__(engine, Config.OBJECTS_LIST_SIZE, Config.OBJECTS_LIST_POS)
        self.selected_obj = None  # !!! Tут лежить об'єкт !!!
        self.items = set()
        self.curr_zindex = 1
        self._get_items()

    def _get_items(self):
        x = Config.OBJECTS_LIST_SIZE[0] // 2
        offset = 20
        for name, img in self._engine.parser.cached_images.items():
            dh = img.get_height() // 2
            offset += dh
            self.items.add(_ObjectListItem(img, name, (x, offset)))
            offset += dh + 10

    def slide_list(self, offset: int | float):
        # Прокручеємо список якщо наведені на нього мишкою
        [obj.rect.move_ip(0, offset * Config.SLIDE_SENSETIVITY) for obj in self.items]

    def _select_obj(self):
        # Беремо об'єкт зі списка
        x, y = pg.mouse.get_pos()
        for obj in self.items:
            if obj.rect.collidepoint(x, y):
                self.selected_obj = obj
                return

    def add_selected_to_world(self, pos: tuple):
        # Додаємо вибраний об'єкт до світу
        # якщо не наведені на жодну з вкладок
        if self._engine.focus_on_world:
            obj = self.selected_obj
            config = {
                'type': 'texture',
                'name': obj.name,
                'size': obj.rect.size,
                'pos': pos,
                'alpha': True,
                'zindex': self.curr_zindex
            }
            self._engine.parser.add_to_world(obj.image, config)

    def keyboard_control(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]: self.slide_list(.2)
        elif keys[pg.K_s]: self.slide_list(-.2)

    def draw(self):
        self._sc.fill('black')
        [self._sc.blit(obj.image, obj.rect) for obj in self.items]
        if self.selected_obj is not None: pg.draw.rect(self._sc, 'red', self.selected_obj.rect.inflate(10, 10), 1)
        self._draw_on_screen()

    def update(self):
        if self.in_focus:
            self.keyboard_control()
            keys = pg.mouse.get_pressed()
            if keys[0]: self._select_obj()


class ObjectEditor(__Tab):
    def __init__(self, engine):
        super().__init__(engine, Config.EDITING_TAB_SIZE, Config.EDITING_TAB_POS)
        self.selected_obj = None
        # Позиція малювання картинки на вкладці
        self._img_pos = self._rect.width // 2, self._rect.height * .1

    def check_focus(self) -> bool:
        super().check_focus()
        # Якщо немає вибраного об'єкта то вкладка не малюється і відповідно
        # в фокусі бути не може
        if not self.selected_obj: self.in_focus = False
        return self.in_focus

    def select_obj(self):
        # Отримуємо оригінальний об'єкт !!!
        self.selected_obj = self._engine.parser.get_collided_rect()

    def _keyboard_control(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]: self.selected_obj.rect.move_ip(0, -1)
        elif keys[pg.K_DOWN]: self.selected_obj.rect.move_ip(0, 1)
        if keys[pg.K_LEFT]: self.selected_obj.rect.move_ip(-1, 0)
        elif keys[pg.K_RIGHT]: self.selected_obj.rect.move_ip(1, 0)

    def draw(self):
        self._sc.fill('black')
        self._sc.blit(self.selected_obj.image, self.selected_obj.image.get_rect(center=self._img_pos))
        self._draw_on_screen()

    def update(self):
        if self.selected_obj:
            self._keyboard_control()
