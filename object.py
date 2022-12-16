import pygame as pg


class StaticObject:
    def __init__(self, img: pg.Surface, pos: list, zindex: int):
        self.image = img
        self.rect = pg.Rect(img.get_rect(center=pos))
        self.zindex = zindex