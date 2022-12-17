import pygame as pg
import json
from config import *


class Texture:
    def __init__(self, img: pg.Surface, **config):
        self.image = pg.transform.scale(img.convert_alpha() if config['alpha'] else img.convert(), config['size'])
        self.rect = pg.Rect(self.image.get_rect(center=config['pos']))
        self.zindex = config['z-index']


class ObjectHandler:
    def __init__(self, game):
        self.sc = game.sc
        self.cached_images = dict()
        self.world = set()
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
                    self.world.add(Texture(img, **obj))
        self.world = sorted(self.world, key=lambda obj: obj.zindex)

    def draw_world(self):
        [self.sc.blit(obj.image, obj.rect) for obj in self.world]


