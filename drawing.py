import pygame as pg
from config import Config


class Drawing:
    def __init__(self, game):
        self._game = game
        self._sc = game.sc
        ##############
        self._fps_font = pg.font.SysFont('arial', 20)

    def _bg(self):
        self._sc.fill('black')

    def _world(self):
        [self._sc.blit(obj.image, obj.rect) for obj in self._game.world.world]

    def _player(self):
        self._game.sc.blit(self._game.player.image, self._game.player.rect)

    def _debug(self):
        if Config.DRAW_TEXTURE_RECT: [pg.draw.rect(self._sc, 'grey', obj.rect, 1) for obj in self._game.world.world]
        if Config.DRAW_PLAYER_RECT: pg.draw.rect(self._sc, 'green', self._game.player.rect, 1)
        if Config.DRAW_CAMERA_RECT: pg.draw.rect(self._sc, 'skyblue', self._game.camera.rect, 2)
        if Config.DRAW_SCREEN_CENTER: pg.draw.circle(self._sc, 'red', Config.CENTER, 3)

    def _fps(self):
        fps = self._fps_font.render(f'{self._game.clock.get_fps(): .1f}', True, Config.FPS_COLOR)
        self._sc.blit(fps, Config.FPS_POS)

    def all(self):
        self._bg()
        self._world()
        self._player()
        self._debug()
        self._fps()
