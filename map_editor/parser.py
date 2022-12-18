import pygame as pg
import json
from config import Config


class Texture:
    def __init__(self, img: pg.Surface, **config):
        self.image = pg.transform.scale(img.convert_alpha() if config['alpha'] else img.convert(), config['size'])
        self.rect = pg.Rect(self.image.get_rect(center=config['pos']))
        self.zindex = config['z-index']


class Object(Texture):
    def __init__(self, img, **config):
        super().__init__(img, **config)
        self.selected = False


class Parser:
    def __init__(self, engine):
        self.engine = engine
        self.cached_images = dict()
        self.current_world = set()
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
                textere = Object(img, **obj)
                self.current_world.add(textere)
        self.current_world = sorted(self.current_world, key=lambda obj: obj.zindex)

    def offset(self, dx: int, dy: int):
        [obj.rect.move_ip(dx, dy) for obj in self.current_world]
