import pygame as pg
import json
from object import StaticObject
from config import *


class ObjectHandler:
    def __init__(self, game):
        self.sc = game.sc
        self._parse_world()

    @staticmethod
    def load_image(path: str, alpha: bool) -> pg.Surface:
        img = pg.image.load(path)
        return img.convert_alpha() if alpha else img.convert()

    @staticmethod
    def resize_image(img: pg.Surface, size: list) -> pg.Surface:
        return pg.transform.scale(img, size)

    def _parse_world(self):
        world = set()
        with open(CURRENT_MAP) as map_:
            map_ = json.load(map_)
            for obj in map_:
                obj_type = obj['type']
                # if obj_type == 'static':
                name = obj['name']
                size = obj['size']
                alpha = obj['alpha']
                img = self.resize_image(self.load_image(f'{STATIC}{name}', alpha), size)
                pos = obj['pos']
                z = obj['z-index']
                world.add(StaticObject(img, pos, z))
            self.world = sorted(world, key=lambda obj: obj.zindex)

    def draw_world(self):
        [self.sc.blit(obj.image, obj.rect) for obj in self.world]


