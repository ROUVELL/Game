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


class ObjectsList(__Tab):
    def __init__(self, engine):
        super().__init__(engine, Config.OBJECTS_LIST_SIZE, Config.OBJECTS_LIST_POS)
        self.selected_obj = None  # !!! Tут лежить індекс !!!
        self._get_imgs_and_rects()

    def _get_imgs_and_rects(self):
        # Зберігаємо оригінальні картинки, збільшені, їхні імена та ректи
        # Оригінальні потрібні при додавані до світу, змаштабовані для відображення в списку, а ректи для відображені на правильній позиції
        self._original_imgs = [img for img in self._engine.parser.cached_images.values()]
        self.names_list = [name for name in self._engine.parser.cached_images.keys()]
        self._rects_list = []
        # TODO: Рефоктор цього костиля!
        offset = 20
        for i, img in enumerate(self._original_imgs):
            w, h = img.get_size()
            coeff = (64 // w)
            w, h = w * coeff, h * coeff
            x, y = Config.OBJECTS_LIST_SIZE[0] // 2, offset
            x, y = x - w // 2, y - h // 2
            self._rects_list.append(pg.Rect(x, y, w, h))
            offset += (h // 64 + h * 1.4)

        self.imgs_list = [pg.transform.scale(self._original_imgs[i], rect.size) for i, rect in enumerate(self._rects_list)]
        # Всі списки збігаються між собою

    def slide_list(self, offset: int):
        # Прокручеємо список якщо наведені на нього мишкою
        [rect.move_ip(0, offset * Config.SLIDE_SENSETIVITY) for rect in self._rects_list]

    def _select_obj(self):
        # Беремо індекс вибраного об'єкта зі списка
        x, y = pg.mouse.get_pos()
        for i, rect in enumerate(self._rects_list): self.selected_obj = i if rect.collidepoint(x, y) else None

    def add_selected_to_world(self, pos: tuple):
        # Додаємо вибраний об'єкт до світу
        if self.selected_obj is None: return
        # якщо не наведені на жодну з вкладок
        if not (self.in_focus or self._engine.editor.in_focus):
            img = self._original_imgs[self.selected_obj]
            w, h = img.get_size()
            self._engine.parser.add_to_world(
                name=self.names_list[self.selected_obj],
                size=(w * 2, h * 2),  # Дефолт, в едіторі можна буде міняти
                pos=pos,  # Центер картинки == позиція мишки
                alpha=True,  # Можна відключити в едіторі
                zindex=1  # TODO: Щось придумати щоб нові об'єкти не були під старими
            )

    def draw(self):
        self._sc.fill('black')
        [self._sc.blit(img, self._rects_list[i]) for i, img in enumerate(self.imgs_list)]
        if self.selected_obj is not None: pg.draw.rect(self._sc, 'red', self._rects_list[self.selected_obj].inflate(10, 10), 2)
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
