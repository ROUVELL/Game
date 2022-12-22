import pygame as pg
import json
import os
from config import Config


# noinspection PyChainedComparisons
def __generate_new_map():
    w_count, h_count = Config.WIDTH_VALUE - 1, Config.HEIGHT_VALUE - 1
    new_world = []
    w = 3
    w -= 1
    for y in range(h_count + 1):
        for x in range(w_count + 1):
            if (w < y < h_count - w) and (w < x < w_count - w):
                continue
            collide = True
            zindex = 1
            alpha = True
            if not x and not y:
                name = 'grass-topleft.png'
            elif not x and y == h_count:
                name = 'grass-bottomleft.png'
            elif x == w_count and not y:
                name = 'grass-topright.png'
            elif x == w_count and y == h_count:
                name = 'grass-bottomright.png'

            elif (not x and 0 < y < h_count) or (x == w_count - w and w < y < h_count - w):
                name = 'grass-left.png'
            elif (x == w_count and 0 < y < h_count) or (x == w and w < y < h_count - w):
                name = 'grass-right.png'
            elif (0 < x < w_count and not y) or (w < x < w_count - w and y == h_count - w):
                name = 'grass-top.png'
            elif (0 < x < w_count and y == h_count) or (w < x < w_count - w and y == w):
                name = 'grass-bottom.png'

            elif x == w == y:
                name = 'grass-topleft-reversed.png'
            elif x == w and y == h_count - w:
                name = 'grass-bottomleft-reversed.png'
            elif x == w_count - w and w == y:
                name = 'grass-topright-reversed.png'
            elif x == w_count - w and y == h_count - w:
                name = 'grass-bottomright-reversed.png'
            else:
                name = 'grass-center.png'
                zindex = 0
                collide = False
                alpha = False
            w, h = Config.TILE_SIZE
            pos = x * w + w // 2, y * h + h // 2
            new_world.append({
                'name': name,
                'pos': pos,
                'size': Config.TILE_SIZE,
                'alpha': alpha,
                'collide': collide,
                'z-index': zindex
            })
    with open(Config.CURRENT_MAP, 'w', encoding='utf-8') as map_:
        new_map = json.dumps(new_world, indent=2)
        map_.write(new_map)

# __generate_new_map()


class Texture:
    def __init__(self, img: pg.Surface, **config):
        self.image = pg.transform.scale(img.convert_alpha() if config['alpha'] else img.convert(), Config.TILE_SIZE)
        self.rect = self.image.get_rect(center=config['pos'])
        self.zindex = config['z-index']


class World:
    def __init__(self):
        self.cached_images = dict()
        self.world = set()
        self.collide_list = []
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
                if obj['collide']:
                    self.collide_list.append(texture.rect)
        self.world = sorted(self.world, key=lambda obj: obj.zindex)

    def offset(self, dx: int, dy: int):
        [obj.rect.move_ip(dx, dy) for obj in self.world]
