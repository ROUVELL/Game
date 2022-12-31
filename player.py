import pygame as pg
from Game.config import Config


class Player:
    def __init__(self, game):
        self._game = game
        # Анімація ходьби по всіх сторонах
        self._front_animation = self._load_animation_by_name('front')
        self._back_animation = self._load_animation_by_name('back')
        self._left_animation = self._load_animation_by_name('left')
        self._right_animation = self._load_animation_by_name('right')
        # Час останнього оновлення та поточний кадр анімації
        self._last_time = pg.time.get_ticks()
        self._frame = 0
        # Картинка для відображення та рект для контролю позиції і колізій
        self.image = self._front_animation[self._frame]
        self.rect = self.image.get_rect(center=Config.CENTER)
        self.zindex = 10
        #####################
        self.direction = 'down'  # Напрям руху
        self.moving = False  # Чи рухаємось
        self.speed = Config.PLAYER_SPEED  # Початкова швидкість

    @staticmethod
    def _load_animation_by_name(name: str):
        # Завантаження анімації
        return [pg.transform.scale(pg.image.load(f'{Config.PLAYER_ANIM}{name}-{i}.png').convert_alpha(), Config.PLAYER_SIZE)
                for i in range(9)]

    def _check_animation_time(self):
        # Перевірка чи не пора змінювати кадр
        now = pg.time.get_ticks()
        if now - self._last_time >= 70:  # 70
            self._last_time = now
            return True

    def _animate(self):
        # Зміна кадру
        self._frame = 0 if not self.moving else self._frame + 1 if self._check_animation_time() else self._frame
        if self._frame > 8: self._frame = 1

        # Зміна картинки в залежності від руху
        match self.direction:
            case 'down': self.image = self._front_animation[self._frame]
            case 'up': self.image = self._back_animation[self._frame]
            case 'left': self.image = self._left_animation[self._frame]
            case 'right': self.image = self._right_animation[self._frame]

    def _movement(self):
        # Рух
        offset = pg.Vector2()
        keys = pg.key.get_pressed()
        self.moving = False
        if keys[pg.K_w]:
            offset.y += -self.speed
            self.direction = 'up'
        if keys[pg.K_s]:
            offset.y += self.speed
            self.direction = 'down'
        if keys[pg.K_a]:
            offset.x += -self.speed
            self.direction = 'left'
        if keys[pg.K_d]:
            offset.x += self.speed
            self.direction = 'right'

        if offset:
            self.moving = True
            if offset.length() > self.speed: offset.scale_to_length(self.speed)  # Корекція руху по діагоналі

        self.rect.move_ip(offset)

    def update(self):
        self._movement()
        self._animate()
