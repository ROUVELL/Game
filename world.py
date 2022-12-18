import pygame as pg
import json
from config import Config


def __generate_new_map():
    offset = 32
    tile_size = 64
    w_count, h_count = Config.WIDTH // tile_size - 1, Config.HEIGHT // tile_size - 1
    new_world = []
    for y in range(h_count + 1):
        for x in range(w_count + 1):
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
            elif not x and 0 < y < h_count:
                name = 'grass-left.png'
            elif x == w_count and 0 < y < h_count:
                name = 'grass-right.png'
            elif 0 < x < w_count and not y:
                name = 'grass-top.png'
            elif 0 < x < w_count and y == h_count:
                name = 'grass-bottom.png'
            else:
                name = 'grass-center.png'
                zindex = 0
                alpha = False
            pos = x * tile_size + offset, y * tile_size + offset
            size = (tile_size, tile_size)
            new_world.append({
                'name': name,
                'pos': pos,
                'size': size,
                'alpha': alpha,
                'z-index': zindex
            })
    with open(Config.CURRENT_MAP, 'w', encoding='utf-8') as map_:
        new_map = json.dumps(new_world, indent=2)
        map_.write(new_map)

# __generate_new_map()


class Texture:
    def __init__(self, img: pg.Surface, **config):
        self.image = pg.transform.scale(img.convert_alpha() if config['alpha'] else img.convert(), config['size'])
        self.rect = pg.Rect(self.image.get_rect(center=config['pos']))
        self.zindex = config['z-index']


class World:
    def __init__(self):
        self.cached_images = dict()
        self.world = set()
        self.parse_world()

    @staticmethod
    def load_image(path: str) -> pg.Surface:
        return pg.image.load(path)

    def parse_world(self, path: str = Config.CURRENT_MAP):
        with open(path) as map_:
            map_ = json.load(map_)
            for obj in map_:
                name = obj['name']
                img = self.cached_images.get(name)
                if not img:
                    img = self.load_image(Config.STATIC + name)
                    self.cached_images[name] = img
                textere = Texture(img, **obj)
                self.world.add(textere)
        self.world = sorted(self.world, key=lambda obj: obj.zindex)

    def offset(self, dx: int, dy: int):
        [obj.rect.move_ip(dx, dy) for obj in self.world]
