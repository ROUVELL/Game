import pygame as pg
from config import Config


class Drawing:
    def __init__(self, game):
        self._game = game
        self._sc = game.sc
        ##############
        self._fps_font = pg.font.SysFont('arial', 20)

    def _world(self):
        [self._sc.blit(obj.image, obj.rect) for obj in self._game.world.textures]

    def _sprites(self):
        sprites = sorted([*self._game.world.sprites, self._game.player], key=lambda obj: obj.rect.centery)
        [self._sc.blit(obj.image, obj.rect) for obj in sprites]

    def _debug(self):
        if Config.DRAW_TEXTURE_RECT: [pg.draw.rect(self._sc, 'grey', obj.rect, 1) for obj in self._game.world.textures]
        if Config.DRAW_SPRITE_RECT: [pg.draw.rect(self._sc, 'grey', obj.rect, 1) for obj in self._game.world.sprites]
        if Config.DRAW_PLAYER_RECT: pg.draw.rect(self._sc, 'green', self._game.player.rect, 1)
        if Config.DRAW_CAMERA_RECT: pg.draw.rect(self._sc, 'skyblue', self._game.camera.rect, 1)
        if Config.DRAW_SCREEN_CENTER: pg.draw.circle(self._sc, 'red', Config.CENTER, 1)
        if Config.DRAW_COORDINATE_AXIS:
            x, y = self._game.world.origin
            w, h = Config.SCREEN
            pg.draw.line(self._sc, 'orange', (0, y), (w, y))
            pg.draw.line(self._sc, 'orange', (x, 0), (x, h))

    def _fps(self):
        fps = self._fps_font.render(f'{self._game.clock.get_fps(): .1f}', True, Config.FPS_COLOR)
        self._sc.blit(fps, Config.FPS_POS)

    def all(self):
        self._sc.fill('black')
        self._world()
        self._sprites()
        self._debug()
        self._fps()
