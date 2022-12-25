import pygame as pg
import json
import os
from config import Config


class _Object:
    def __init__(self, img, **config):
        self.config = config
        self.image = pg.transform.scale(img.convert_alpha() if config['alpha'] else img.convert(), config['size'])
        self.rect = self.image.get_rect(center=config['pos'])
        self.zindex = config['zindex']

    def __repr__(self):
        return {
            'name': self.config['name'],
            'size': self.image.get_size(),
            'pos': self.rect.center,
            'alpha': self.config['alpha'],
            'zindex': self.zindex
        }


class Parser:
    def __init__(self, engine):
        self._engine = engine
        self.cached_images = dict()
        self.current_world = []  # Можна set()
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

    def add_to_world(self, **config):
        # Додавання новога тайла до світу. Пересортувати для правильного відображення
        img = self.cached_images[config['name']]
        self.current_world.append(_Object(img, **config))
        self._sort_world()

    def save_world(self):
        with open(Config.CURRENT_MAP, 'w', encoding='utf-8') as map_:
            m = json.dumps([tile.__repr__() for tile in self.current_world], indent=2)
            map_.write(m)
        print('Saved!')
