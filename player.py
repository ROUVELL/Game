import pygame as pg
from config import Config


class Player:
    def __init__(self, game):
        self.game = game
        self.front_animation = [self._load_and_scale_img(f'front-{i}.png') for i in range(9)]
        self.back_animation = [self._load_and_scale_img(f'back-{i}.png') for i in range(9)]
        self.left_animation = [self._load_and_scale_img(f'left-{i}.png') for i in range(9)]
        self.right_animation = [self._load_and_scale_img(f'right-{i}.png') for i in range(9)]
        self.last_time = pg.time.get_ticks()
        self.frame = 0
        self.image = self.front_animation[self.frame]
        self.rect = self.image.get_rect(center=Config.CENTER)
        self.direction = 'down'
        self.moving = False
        self.speed = Config.PLAYER_SPEED

    @staticmethod
    def _load_and_scale_img(name: str):
        return pg.transform.scale(pg.image.load(f'{Config.PLAYER_ANIM}{name}').convert_alpha(), Config.PLAYER_SIZE)

    def check_animation_time(self):
        now = pg.time.get_ticks()
        if now - self.last_time >= 70:  # 70
            self.last_time = now
            return True
        return False

    def texture_collide(self, dx: int, dy: int):
        target = self.rect.move_ip(dx, dy)
        collided = target.collidelistall(self.game.world.collide_list)
        for i in collided:
            rect = self.game.world.collide_list[i]
            delta_x = target.left - rect.right
            delta_y = target.top - rect.bottom

            print(delta_x, delta_y)


    def animate(self):
        # if moving:
        #     if self.check_animation_time():
        #         self.frame += 1
        # else:
        #     self.frame = 0
        self.frame = 0 if not self.moving else self.frame + 1 if self.check_animation_time() else self.frame
        if self.frame > 8:
            self.frame = 1

        match self.direction:
            case 'down':
                self.image = self.front_animation[self.frame]
            case 'up':
                self.image = self.back_animation[self.frame]
            case 'left':
                self.image = self.left_animation[self.frame]
            case 'right':
                self.image = self.right_animation[self.frame]

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
            self.direction = 'left'
        if keys[pg.K_d]:
            dx += self.speed
            self.moving = True
            self.direction = 'right'

        self.texture_collide(dx, dy)

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        self.movement()
        self.animate()
