import pygame as pg
import json
import os
from config import Config


class Texture:
    def __init__(self, img: pg.Surface, **config):
        self.image = pg.transform.scale(img.convert_alpha() if config['alpha'] else img.convert(), config['size'])
        self.rect = self.image.get_rect(center=config['pos'])
        self.zindex = config['zindex']


class World:
    def __init__(self):
        self.world = set()
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
                self.world.add(Texture(img, **obj))
        self.world = sorted(self.world, key=lambda obj: obj.zindex)

    def offset_world(self, dx: int, dy: int):
        # Рухаємо весь світ
        [obj.rect.move_ip(dx, dy) for obj in self.world]
