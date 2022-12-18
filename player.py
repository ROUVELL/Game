import pygame as pg
from config import Config


class Player:
    def __init__(self, game):
        self.game = game
        self.front_animation = [self._load_and_scale_img(f'{Config.PLAYER_ANIM}front-{i}.png') for i in range(1)]
        self.image = self.front_animation[0]
        self.rect = self.image.get_rect(center=Config.CENTER)

    def _load_and_scale_img(self, path: str):
        return pg.transform.scale(pg.image.load(path).convert_alpha(), Config.PLAYER_SIZE)

    def draw(self):
        self.game.sc.blit(self.image, self.rect)