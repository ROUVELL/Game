import pygame as pg
from pygame import Vector2 as vec
from config import Config

import json
import os


class _Object:
    def __init__(self, img: pg.Surface, **config):
        self.image = pg.transform.scale(img.convert_alpha() if config['alpha'] else img.convert(), config['size'])
        self.rect = self.image.get_rect(center=config['pos'])
        self.zindex = config['zindex']


class World:
    def __init__(self):
        self.textures = []
        self.sprites = []
        self.origin = vec(Config.CENTER)
        self._cache_images()
        self.parse_world()

    def _cache_images(self):
        # Кешування всіх статичних тайлів
        self.cached_images = {name: pg.image.load(Config.STATIC + name) for name in os.listdir(Config.STATIC)}

    def parse_world(self, path: str = Config.CURRENT_MAP):
        # Відкриваємь вибрану карту, створюємо список тайлів та відсортовуємо його по z індексу
        with open(path) as map_:
            for obj in json.load(map_):
                img = self.cached_images[obj['name']]
                obj['pos'] = vec(obj['pos']) + self.origin
                match obj['type']:
                    case 'texture': self.textures.append(_Object(img, **obj))
                    case 'sprite': self.sprites.append(_Object(img, **obj))
                    case _: raise TypeError(f"Unknown type of {obj}")
        self.textures = sorted(self.textures, key=lambda obj: obj.zindex)
        self.sprites = sorted(self.sprites, key=lambda obj: obj.zindex)

    def offset_world(self, dx: int, dy: int):
        # Рухаємо весь світ
        self.origin.x += dx
        self.origin.y += dy
        [obj.rect.move_ip(dx, dy) for obj in [*self.textures, *self.sprites]]
