import pygame as pg
from config import Config


class Camera:
    def __init__(self, game):
        self._game = game
        self._world = game.world
        self._target = game.player
        self.rect = pg.Rect(Config.CAMERA_RECT)

    def _get_offset(self) -> pg.Vector2:
        # Колізія з камерою і зміщення в залежності від неї
        ox = oy = 0
        camera, player = self.rect, self._target.rect

        if camera.left > player.left: ox = camera.left - player.left
        elif camera.right < player.right: ox = camera.right - player.right
        if camera.top > player.top: oy = camera.top - player.top
        elif camera.bottom < player.bottom: oy = camera.bottom - player.bottom
        return pg.Vector2(ox, oy)

    def update(self):
        if not self.rect.contains(self._target):  # Чи не виходить ігрок за межі камери
            offset = self._get_offset()
            self._target.rect.move_ip(offset)
            self._world.offset_world(offset)
