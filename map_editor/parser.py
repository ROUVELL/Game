import pygame as pg
import json
import os
from config import Config


class _Object:
    def __init__(self, img: pg.Surface, **config):
        self.name = config['name']
        self._orig_image = img
        self._orig_rect = img.get_rect()
        self.alpha = config['alpha']
        self.zindex = config['zindex']
        self._get_image(config['size'])
        self.rect = self.image.get_rect(center=config['pos'])

    def _get_image(self, size: tuple):
        self.image = pg.transform.scale(self._orig_image.convert_alpha() if self.alpha else img.convert(), size)

    def scale(self, offset: float):
        w, h = self._orig_rect.width * offset, self._orig_rect.height * offset
        self.rect.size = (w, h)
        self._get_image(self.rect.size)

    def __repr__(self):
        return {
            'name': self.name,
            'size': self.image.get_size(),
            'pos': self.rect.center,
            'alpha': self.alpha,
            'zindex': self.zindex
        }


class Parser:
    def __init__(self, engine):
        self._engine = engine
        self.cached_images = dict()
        self.current_world = []  # Можна set()
        self.scale_coeff = 1
        self._cache_images()
        self.parse_world()

    @staticmethod
    def _load_image(path: str) -> pg.Surface:
        return pg.image.load(path)

    def _cache_images(self):
        # Кешуємо всі статичні картинки
        for name in os.listdir(Config.STATIC):
            img = self._load_image(Config.STATIC + name)
            self.cached_images[name] = img

    def _sort_world(self):
        # Сортування по z індексу
        self.current_world = sorted(self.current_world, key=lambda obj: obj.zindex)

    def parse_world(self, path: str = Config.CURRENT_MAP):
        # Відкриваємо вибрану карту, зберігаємо кожен тайл і відсортовуємо
        with open(path) as map_:
            map_ = json.load(map_)
            for obj in map_:
                img = self.cached_images[obj['name']]
                textere = _Object(img, **obj)
                self.current_world.append(textere)
        self._sort_world()

    def offset(self, dx: int, dy: int):
        # Зміна позиції всіх тайлів
        [obj.rect.move_ip(dx, dy) for obj in self.current_world]

    def scale(self, offset: float):
        # Зміна розмірів всіх тайлів
        self.scale_coeff += offset
        self.scale_coeff = min(max(self.scale_coeff, .2), 8)
        for obj in self.current_world:
            obj.scale(self.scale_coeff)

    def add_to_world(self, **config):
        # Додавання новога тайла до світу. Пересортувати для правильного відображення
        img = self.cached_images[config['name']]
        obj = _Object(img, **config)
        obj.scale(self.scale_coeff)
        self.current_world.append(obj)
        self._sort_world()

    def save_world(self):
        # Збереження світу
        with open(Config.CURRENT_MAP, 'w', encoding='utf-8') as map_:
            m = json.dumps([tile.__repr__() for tile in self.current_world], indent=2)
            map_.write(m)
