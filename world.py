import pygame as pg
import json
import os
from config import Config


class Texture:
    def __init__(self, img: pg.Surface, **config):
        self.image = pg.transform.scale(img.convert_alpha() if config['alpha'] else img.convert(), Config.TILE_SIZE)
        self.rect = self.image.get_rect(center=config['pos'])
        self.zindex = config['z-index']


class World:
    def __init__(self):
        self.cached_images = dict()
        self.world = set()
        # self.collide_list = []
        self.cache_images()
        self.parse_world()

    @staticmethod
    def load_image(path: str) -> pg.Surface:
        return pg.image.load(path)

    def cache_images(self):
        for name in os.listdir(Config.STATIC):
            self.cached_images[name] = self.load_image(Config.STATIC + name)

    def parse_world(self, path: str = Config.CURRENT_MAP):
        with open(path) as map_:
            map_ = json.load(map_)
            for obj in map_:
                img = self.cached_images[obj['name']]
                texture = Texture(img, **obj)
                self.world.add(texture)
                # if obj['collide']:
                #     self.collide_list.append(texture.rect)
        self.world = sorted(self.world, key=lambda obj: obj.zindex)

    def offset(self, dx: int, dy: int):
        [obj.rect.move_ip(dx, dy) for obj in self.world]
