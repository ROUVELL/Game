import pygame as pg
import json
from object import StaticObject
from config import *


class ObjectHandler:
    def __init__(self, game):
        self.sc = game.sc
        self.cached_images = dict()
        self.static_objs_list = set()
        self._parse_world()

    @staticmethod
    def load_image(path: str) -> pg.Surface:
        return pg.image.load(path)

    def _parse_world(self):
        with open(Config.CURRENT_MAP) as map_:
            map_ = json.load(map_)
            for obj in map_:
                if obj['type'] == 'static':
                    name = obj['name']
                    img = self.cached_images.get(name)
                    if not img:
                        img = self.load_image(Config.STATIC + name)
                        self.cached_images[name] = img
                    self.static_objs_list.add(StaticObject(img, **obj))
        self.static_objs_list = sorted(self.static_objs_list, key=lambda obj: obj.zindex)

    def draw_world(self):
        [self.sc.blit(obj.image, obj.rect) for obj in self.static_objs_list]


