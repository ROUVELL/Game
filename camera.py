import pygame as pg
from config import Config


class Camera:
    def __init__(self, game):
        self.game = game
        self.world = game.world
        self.target = game.player.rect
        self.rect = pg.Rect(Config.CAMERA_RECT)

    def check_collide_and_get_offset(self) -> tuple:
        # Колізія з камерою і зміщення в залежності від неї
        ox = oy = 0
        if self.rect.left > self.target.left:
            ox = self.rect.left - self.target.left
        if self.rect.right < self.target.right:
            ox = self.rect.right - self.target.right
        if self.rect.top > self.target.top:
            oy = self.rect.top - self.target.top
        if self.rect.bottom < self.target.bottom:
            oy = self.rect.bottom - self.target.bottom
        return ox, oy

    def update(self):
        if not self.rect.contains(self.target):  # Чи не виходить ігрок за межі камери
            ox, oy = self.check_collide_and_get_offset()

            self.target.move_ip(ox, oy)
            self.world.offset(ox, oy)
