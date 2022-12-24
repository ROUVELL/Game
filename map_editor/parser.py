import pygame as pg
import json
import os
from config import Config


class _Object:
    def __init__(self, img, **config):
        self.image = pg.transform.scale(img.convert_alpha() if config['alpha'] else img.convert(), Config.TILE_SIZE)
        self.rect = pg.Rect(self.image.get_rect(center=config['pos']))
        self.zindex = config['z-index']
        ################


class Parser:
    def __init__(self, engine):
        self._engine = engine
        self._cached_images = dict()
        self.current_world = set()
        self.cache_images()
        self.parse_world()

    @staticmethod
    def _load_image(path: str) -> pg.Surface:
        return pg.image.load(path)

    def cache_images(self):
        for name in os.listdir(Config.STATIC):
            img = self._load_image(Config.STATIC + name)
            self._cached_images[name] = img

    def parse_world(self, path: str = Config.CURRENT_MAP):
        with open(path) as map_:
            map_ = json.load(map_)
            for obj in map_:
                img = self._cached_images[obj['name']]
                textere = _Object(img, **obj)
                self.current_world.add(textere)
        self.current_world = sorted(self.current_world, key=lambda obj: obj.zindex)

    def offset(self, dx: int, dy: int):
        [obj.rect.move_ip(dx, dy) for obj in self.current_world]
