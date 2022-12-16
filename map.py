import pygame as pg
from config import *
import json


class Map:
    def __init__(self, game):
        self.game = game
        with open(CURRENT_MAP) as map_:
            map_ = json.load(map_)['map']
            self.world = self.get_world(map_)

    @staticmethod
    def load_image(name: str, is_alpha: bool = False) -> pg.Surface:
        img = pg.image.load(f'{STATIC}{name}')
        return img.convert() if not is_alpha else img.convert_alpha()

    @staticmethod
    def scale_image(img: pg.Surface, size: tuple) -> pg.Surface:
        return pg.transform.scale(img, size)

    def get_world(self, map_: list) -> dict:
        world = dict()
        with open(STATIC_CONFIG, encoding='utf-8') as static_config:
            static_config = json.load(static_config)
            for y, row in enumerate(map_):
                for x, char in enumerate(row):
                    if char in static_config.keys():
                        config = static_config[char]
                        img = self.load_image(config['name'], config['is_alpha'])
                        if config.get('size'):
                            size = config['size']
                            img = self.scale_image(img, size)
                        if config.get('scale'):
                            scale = config['scale']
                            w, h = img.get_size()
                            size = int(w * scale), int(h * scale)
                            img = self.scale_image(img, size)
                        w, h = img.get_size()
                        pos = x * w, y * h
                        world[pos] = img
        return world

    def draw_world(self):
        [self.game.sc.blit(img, pos) for pos, img in self.world.items()]