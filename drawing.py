import pygame as pg


class Drawing:
    def __init__(self, game):
        self.game = game
        ##############
        self.fps_font = pg.font.SysFont('arial', 30)

    def world(self):
        pass

    def player(self):
        pass

    def debug(self):
        pass

    def fps(self):
        pass

    def all(self):
        self.world()
        self.player()
        self.debug()
        self.fps()