import pygame as pg
from config import Config


class Camera:
    def __init__(self, game):
        self.game = game
        self.textures = game.world.get_world()
        self.target = game.player
        self.rect = (0, 0, *Config.SCREEN)

    def update(self):
        pass

