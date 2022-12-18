import pygame as pg
from config import Config


class Player:
    def __init__(self, game):
        self.game = game
        self.front_animation = [self._load_and_scale_img(f'{Config.PLAYER_ANIM}front-{i}.png') for i in range(9)]
        self.last_time = pg.time.get_ticks()
        self.frame = 0
        self.image = self.front_animation[self.frame]
        self.rect = self.image.get_rect(center=Config.CENTER)
        self.direction = 'down'
        self.moving = False
        self.speed = 5

    def _load_and_scale_img(self, path: str):
        return pg.transform.scale(pg.image.load(path).convert_alpha(), Config.PLAYER_SIZE)

    def animate(self):
        if self.moving:
            now = pg.time.get_ticks()
            if now - self.last_time >= 80:
                self.last_time = now
                self.frame += 1
                if self.frame > 8:
                    self.frame = 0
        else:
            self.frame = 0
        match self.direction:
            case 'down':
                self.image = self.front_animation[self.frame]

    def movement(self):
        dx = dy = 0
        keys = pg.key.get_pressed()
        self.moving = False
        if keys[pg.K_w]:
            dy += -self.speed
            self.moving = True
            self.direction = 'up'
        if keys[pg.K_s]:
            dy += self.speed
            self.moving = True
            self.direction = 'down'
        if keys[pg.K_a]:
            dx += -self.speed
            self.moving = True
            self.direction = 'right'
        if keys[pg.K_d]:
            dx += self.speed
            self.moving = True
            self.direction = 'left'

        self.rect.centerx += dx
        self.rect.centery += dy

    def update(self):
        self.movement()
        self.animate()

    def draw(self):
        self.game.sc.blit(self.image, self.rect)