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

    def check_focus(self):
        self.in_focus = self._rect.collidepoint(*pg.mouse.get_pos())
        return self.in_focus

    def _draw_on_screen(self):
        self._engine.app.sc.blit(self._sc, self._rect)
        # if self.in_focus:
        #     pg.draw.rect(self._engine.app.sc, 'green', self._rect, 1, 10)


class _ObjectListItem:
    def __init__(self, img: pg.Surface, name: str, pos: tuple, alpha: bool = True, zindex: int = 1):
        self.name = name
        self.image = img.convert_alpha() if alpha else img.convert()
        self.rect = img.get_rect(center=pos)
        self.alpha = alpha
        self.zindex = zindex


class ObjectsList(__Tab):
    def __init__(self, engine):
        super().__init__(engine, Config.OBJECTS_LIST_SIZE, Config.OBJECTS_LIST_POS)
        self.selected_obj = None  # !!! Tут лежить об'єкт !!!
        self.items = set()
        self._get_items()

    def _get_items(self):
        # TODO: Виправити цей мазохізм інакше я поїду кукушкою
        self.items = set()
        x = Config.OBJECTS_LIST_SIZE[0] // 2
        offset = 0
        for name, img in self._engine.parser.cached_images.items():
            offset += img.get_height() + 10
            self.items.add(_ObjectListItem(img, name, (x, offset)))
            offset += 10

    def slide_list(self, offset: int):
        # Прокручеємо список якщо наведені на нього мишкою
        [obj.rect.move_ip(0, offset * Config.SLIDE_SENSETIVITY) for obj in self.items]

    def _select_obj(self):
        # Беремо індекс вибраного об'єкта зі списка
        x, y = pg.mouse.get_pos()
        for obj in self.items:
            if obj.rect.collidepoint(x, y):
                self.selected_obj = obj
                return

    def add_selected_to_world(self, pos: tuple):
        # Додаємо вибраний об'єкт до світу
        if self.selected_obj is None: return
        # якщо не наведені на жодну з вкладок
        if self._engine.focus_on_world:
            obj = self.selected_obj
            config = {
                'name': obj.name,
                'size': obj.rect.size,
                'pos': pos,
                'alpha': obj.alpha,
                'zindex': obj.zindex
            }
            self._engine.parser.add_to_world(obj.image, config)

    def draw(self):
        self._sc.fill('black')
        [self._sc.blit(obj.image, obj.rect) for obj in self.items]
        if self.selected_obj is not None: pg.draw.rect(self._sc, 'red', self.selected_obj.rect.inflate(10, 10), 1)
        self._draw_on_screen()

    def update(self):
        keys = pg.mouse.get_pressed()
        if keys[0] and self.in_focus: self._select_obj()


class Editor(__Tab):
    def __init__(self, engine):
        super().__init__(engine, Config.EDITING_TAB_SIZE, Config.EDITING_TAB_POS)

    def draw(self):
        self._draw_on_screen()

    def update(self):
        pass
