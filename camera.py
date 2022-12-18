import pygame as pg
from config import Config


class Camera:
    def __init__(self, game):
        self.game = game
        self.world = game.world
        self.target = game.player.rect
        self.rect = pg.Rect(Config.CAMERA_RECT)

    def update(self):
        ox = oy = 0
        if not self.rect.contains(self.target):  # Чи не виходить ігрок за межі камери
            if self.rect.left > self.target.left:
                ox = self.rect.left - self.target.left
            if self.rect.right < self.target.right:
                ox = self.rect.right - self.target.right
            if self.rect.top > self.target.top:
                oy = self.rect.top - self.target.top
            if self.rect.bottom < self.target.bottom:
                oy = self.rect.bottom - self.target.bottom

            self.target.x += ox
            self.target.y += oy
            self.world.offset(ox, oy)

    def draw(self):
        if Config.DRAW_CAMERA_RECT:
            pg.draw.rect(self.game.sc, 'orange', self.rect, 2)

