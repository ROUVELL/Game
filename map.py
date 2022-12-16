import pygame as pg
from config import *


map_ = [
    ['G-TL', 'G-T', 'G-T', 'G-T', 'G-T', 'G-T', 'G-T', 'G-T', 'G-T', 'G-T', 'G-T', 'G-T', 'G-T', 'G-T', 'G-TR'],
    ['G-L', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-R'],
    ['G-L', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-R'],
    ['G-L', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-R'],
    ['G-L', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-R'],
    ['G-L', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-R'],
    ['G-L', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-R'],
    ['G-L', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-R'],
    ['G-L', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-R'],
    ['G-L', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-R'],
    ['G-L', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-R'],
    ['G-L', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-R'],
    ['G-L', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-C', 'G-R'],
    ['G-BL', 'G-B', 'G-B', 'G-B', 'G-B', 'G-B', 'G-B', 'G-B', 'G-B', 'G-B', 'G-B', 'G-B', 'G-B', 'G-B', 'G-BR']
]


class Map:
    def __init__(self, game):
        self.game = game
        self.world = self.get_world(map_)

    def load_image(self, name: str, is_alpha: bool = False) -> pg.Surface:
        img = pg.image.load(f'{TILES_PATH}{name}')
        return img.convert() if not is_alpha else img.convert_alpha()

    def scale_image(self, img: pg.Surface, size: tuple) -> pg.Surface:
        return pg.transform.scale(img, size)

    def get_world(self, map_: list) -> dict:
        world = dict()
        for y, row in enumerate(map_):
            for x, char in enumerate(row):
                if char in TILES.keys():
                    config = TILES[char]
                    img = self.load_image(config['name'], config['is_alpha'])
                    w, h = img.get_size()
                    if config.get('size'):
                        size = config['size']
                        img = self.scale_image(img, size)
                        w, h = img.get_size()
                    if config.get('scale'):
                        scale = config['scale']
                        size = int(w * scale), int(h * scale)
                        img = self.scale_image(img, size)
                        w, h = img.get_size()
                    pos = x * w, y * h
                    world[pos] = img
        return world

    def draw_world(self):
        [self.game.sc.blit(img, pos) for pos, img in self.world.items()]