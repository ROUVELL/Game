import pygame as pg
from config import Config

import json
import os


class _Object:
    def __init__(self, img: pg.Surface, **config):
        self.image = img.convert_alpha() if config['alpha'] else img.convert()
        self.rect = self.image.get_rect(center=config['pos'])
        self.zindex = config['zindex']


class World:
    def __init__(self):
        self.textures = []
        self.sprites = []
        self.origin = pg.Vector2(Config.CENTER)
        self._cache_images()
        self.parse_world()

    def _cache_images(self):
        # Кешування всіх статичних тайлів
        self.cached_images = {name: pg.image.load(Config.STATIC + name) for name in os.listdir(Config.STATIC)}

    def parse_world(self, path: str = Config.CURRENT_MAP):
        # Відкриваємо вибрану карту, створюємо список тайлів та відсортовуємо його по z індексу
        with open(path) as map_:
            for obj in json.load(map_):
                img = self.cached_images[obj['name']]
                obj['pos'] = pg.Vector2(obj['pos']) + self.origin
                match obj['type']:
                    case 'texture': self.textures.append(_Object(img, **obj))
                    case 'sprite': self.sprites.append(_Object(img, **obj))
                    case _: raise TypeError(f"Unknown object: {obj}")
        self.textures.sort(key=lambda obj: obj.zindex)
        self.sprites.sort(key=lambda obj: obj.zindex)

    def offset_world(self, offset: pg.Vector2):
        # Рухаємо весь світ
        self.origin.x += offset.x
        self.origin.y += offset.y
        [obj.rect.move_ip(offset) for obj in [*self.textures, *self.sprites]]
