import pygame as pg
from config import Config


class Button:
    def __init__(self, text: str, pos: tuple, func):
        self._text = pg.font.Font(Config.INFO_FONT, 14).render(text, 0, 'white')
        self._text_rect = self._text.get_rect(center=pos)
        images = ('button-default.png', 'button-hovered.png', 'button-clicked.png', 'button-disabled.png')
        images = [pg.image.load(f'{Config.UI}{name}').convert_alpha() for name in images]
        imgs_and_rects = [(img, img.get_rect(center=pos)) for img in images]
        self._statuses = {
            'default': imgs_and_rects[0],
            'hover': imgs_and_rects[1],
            'click': imgs_and_rects[2],
            'disable': imgs_and_rects[3]
        }
        self._status = 'default'
        self._func = func
        self._last = pg.time.get_ticks()
        self._set_status()

    def _set_status(self):
        self._image, self._rect = self._statuses[self._status]

    def _check_time(self):
        now = pg.time.get_ticks()
        if now - self._last > 100:
            self._last = now
            return True

    def _check_status(self):
        if self._status == 'click' and not self._check_time(): return
        self._status = 'default'
        if self._rect.collidepoint(*pg.mouse.get_pos()):
            self._status = 'hover'
            if pg.mouse.get_pressed()[0] and self._check_time():
                self._status = 'click'
                self._func()
        self._set_status()

    def update(self):
        if self._status == 'disable': return
        self._check_status()

    def draw(self, sc):
        sc.blit(self._image, self._rect)
        sc.blit(self._text, self._text_rect)