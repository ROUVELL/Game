import pygame as pg
from config import Config


class Drawing:
    def __init__(self, game):
        self.game = game
        self.sc = game.sc
        ##############
        self.fps_font = pg.font.SysFont('arial', 30)

    def bg(self):
        self.sc.fill('black')

    def world(self):
        [self.sc.blit(obj.image, obj.rect) for obj in self.game.world.world]

    def player(self):
        self.game.sc.blit(self.game.player.image, self.game.player.rect)

    def debug(self):
        if Config.DRAW_TEXTURE_RECT:
            [pg.draw.rect(self.sc, 'grey', obj.rect, 1) for obj in self.game.world.world]
        if Config.DRAW_PLAYER_RECT:
            pg.draw.rect(self.game.sc, 'green', self.game.player.rect, 1)
        if Config.DRAW_CAMERA_RECT:
            pg.draw.rect(self.game.sc, 'skyblue', self.game.camera.rect, 2)

    def fps(self):
        fps = self.fps_font.render(f'{self.game.clock.get_fps(): .1f}', True, Config.FPS_COLOR)
        self.sc.blit(fps, Config.FPS_POS)

    def all(self):
        self.bg()
        self.world()
        self.player()
        self.debug()
        self.fps()
