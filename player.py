import pygame as pg
from config import Config


class Player:
    def __init__(self, game):
        self.game = game
        # Анімація ходьби по всіх сторонах
        self.front_animation = [self._load_and_scale_img(f'front-{i}.png') for i in range(9)]
        self.back_animation = [self._load_and_scale_img(f'back-{i}.png') for i in range(9)]
        self.left_animation = [self._load_and_scale_img(f'left-{i}.png') for i in range(9)]
        self.right_animation = [self._load_and_scale_img(f'right-{i}.png') for i in range(9)]
        # Час останнього оновлення та поточний кадр анімації
        self.last_time = pg.time.get_ticks()
        self.frame = 0
        # Картинка для відображення та рект для контролю позиції і колізій
        self.image = self.front_animation[self.frame]
        self.rect = self.image.get_rect(center=Config.CENTER)
        # Напрям руху, чи в русі та поточна швидкість
        self.direction = 'down'
        self.moving = False
        self.speed = Config.PLAYER_SPEED

    @staticmethod
    def _load_and_scale_img(name: str):
        # Завантаження анімації
        return pg.transform.scale(pg.image.load(f'{Config.PLAYER_ANIM}{name}').convert_alpha(), Config.PLAYER_SIZE)

    def check_animation_time(self):
        # Перевірка чи не пора змінювати кадр
        now = pg.time.get_ticks()
        if now - self.last_time >= 70:  # 70
            self.last_time = now
            return True
        return False

    # Not using!
    # def texture_collide(self, dx: int, dy: int):
    #     target = self.rect.move(dx, dy)
    #     collided = target.collidelistall(self.game.world.collide_list)
    #     for i in collided:
    #         rect = self.game.world.collide_list[i]
    #         delta_x = target.left - rect.right
    #         delta_y = target.top - rect.bottom
    #
    #     self.rect.move_ip(dx, dy)


    def animate(self):
        # Зміна кадру
        self.frame = 0 if not self.moving else self.frame + 1 if self.check_animation_time() else self.frame
        if self.frame > 8:
            self.frame = 1

        # Зміна картинки в залежності від руху
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
        # Рух
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

        self.rect.move_ip(dx, dy)
        # self.texture_collide(dx, dy)

    def update(self):
        self.movement()
        self.animate()
