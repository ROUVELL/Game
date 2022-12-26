import pygame as pg
from config import Config


class __Tab:
    def __init__(self, engine, size: tuple, pos: tuple):
        self._engine = engine
        self._sc = pg.Surface(size)
        self._sc.set_alpha(200)
        self._rect = self._sc.get_rect(topleft=pos)
        self.in_focus = False  # Чи наведена мишка

    def check_focus(self):
        self.in_focus = self._rect.collidepoint(*pg.mouse.get_pos())

    def draw_on_screen(self):
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
        self.imgs_list = [pg.transform.scale2x(img) for img in self._original_imgs]
        self.rects_list = [img.get_rect(center=(Config.OBJECTS_LIST_SIZE[0] // 2, i * 96 + 96)) for i, img in enumerate(self.imgs_list)]
        # Список імен, картинок і ректів збігаються між собою

    def slide_list(self, offset: int):
        # Прокручеємо список якщо наведені на нього мишкою
        [rect.move_ip(0, offset * Config.SLIDE_SENSETIVITY) for rect in self.rects_list]

    def _select_obj(self):
        # Вибираємо об'єкт з списка
        x, y = pg.mouse.get_pos()
        for i, rect in enumerate(self.rects_list):
            if rect.collidepoint(x, y):
                return i

    def add_selected_to_world(self, pos: tuple):
        # Додаємо об'єкт до світу якщо ми наведені на нього
        # Якщо немає вибраного об'єкта - функція не визветься
        if not (self.in_focus or self._engine.editor.in_focus):
            img = self._original_imgs[self.selected_obj]
            self._engine.parser.add_to_world(
                name=self.names_list[self.selected_obj],
                size=(64, 64),  # Дефолт, в едіторі можна буде міняти
                pos=pos,  # Центер картинки == позиція мишки
                alpha=True,  # Можна відключити в едіторі
                zindex=1  # TODO: Щось придумати щоб нові об'єкти не були під старими
            )

    def draw(self):
        self._sc.fill('black')
        for i, img in enumerate(self.imgs_list):
            self._sc.blit(img, self.rects_list[i])
        if self.selected_obj is not None:
            pg.draw.rect(self._sc, 'red', self.rects_list[self.selected_obj].inflate(10, 10), 2)

        self.draw_on_screen()

    def update(self):
        keys = pg.mouse.get_pressed()
        if keys[0]:
            if self.in_focus:  # Якщо ми навелись мишою то дивимось що ми вибрали
                self.selected_obj = self._select_obj()


class Editor(__Tab):
    def __init__(self, engine):
        super().__init__(engine, Config.EDITING_TAB_SIZE, Config.EDITING_TAB_POS)

    def update(self):
        pass
