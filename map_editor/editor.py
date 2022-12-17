import pygame as pg
import json
from config import *


class Editor:
    def __init__(self, game):
        self.sc = game.sc
        self.clock = game.clock
        self.running = True

    def events(self):
        for event in pg.event.get():
            self.running = False if event.type == pg.KEYUP and event.key == pg.K_ESCAPE else True

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.sc.fill('black')
            pg.display.flip()
