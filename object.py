import pygame as pg


class StaticObject:
    def __init__(self, img: pg.Surface, **config):
        self.image = pg.transform.scale(img.convert_alpha() if config['alpha'] else img.convert(), config['size'])
        self.rect = pg.Rect(self.image.get_rect(center=config['pos']))
        self.zindex = config['z-index']