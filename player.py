import pygame as pg
from config import Config

from math import atan, pi


class Player:
    def __init__(self, game):
        self._game = game
        # Анімація ходьби по всіх сторонах
        self.walk_anim = self._load_animation('walking', 8)
        # Анімація стрільби з лука
        self.bow_anim = self._load_animation('bow', 13)
        # Час останнього оновлення та поточний кадр анімації
        self._last_time = pg.time.get_ticks()
        self._frame = 0
        # Картинка для відображення та рект для контролю позиції і колізій
        self.curr_animation = self.walk_anim
        self.image = self.curr_animation['down'][self._frame]
        self.rect = self.image.get_rect(center=Config.CENTER)
        #####################
        self.direction = 'down'  # Напрям руху
        self.angle = 0       # Кут миші
        self.moving = False  # Чи рухаємось
        self.attack = False  # Чи атакуємо
        self.speed = Config.PLAYER_SPEED  # Початкова швидкість

    @staticmethod
    def _load_animation(directory: str, lenght: int) -> dict[str: list | int]:
        # Завантаження анімації
        res = {'lenght': lenght}
        for name in ['up', 'right', 'left', 'down']:
            res[name] = [pg.image.load(f'{Config.PLAYER_ANIM}{directory}/{name}-{i}.png').convert_alpha()
                         for i in range(lenght)]
        return res

    def _check_animation_time(self):
        # Перевірка чи не пора змінювати кадр
        now = pg.time.get_ticks()
        if now - self._last_time >= 70:  # 70
            self._last_time = now
            return True

    def _check_curr_animation(self):
        if self.attack:
            self.curr_animation = self.bow_anim
        elif self.moving:
            self.curr_animation = self.walk_anim

    def _animate(self):
        # Зміна кадру
        if self.moving or self.attack:
            if self._check_animation_time():
                self._frame += 1
        else: self._frame = 0
        if self._frame == self.curr_animation['lenght']:
            self._frame = 0
            if self.attack:
                if pg.mouse.get_pressed()[0]:
                    self._frame = 3
                else:
                    self.attack = False
                    self.curr_animation = self.walk_anim

        # Зміна картинки в залежності від руху
        self.image = self.curr_animation[self.direction][self._frame]
        self.rect = self.image.get_rect(center=self.rect.center)

    def _movement(self):
        # Рух
        self.moving = False

        if self.attack: return

        offset = pg.Vector2()
        keys = pg.key.get_pressed()
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

    def _check_view_direction(self):
        mx, my = pg.mouse.get_pos()
        px, py = self.rect.center
        dx, dy = mx - px, my - py
        # TODO: Знайти кут за позюцією мишки


    def _check_attack(self):
        if self.attack: return
        keys = pg.mouse.get_pressed()
        if keys[0]:
            self.attack = True

    def update(self):
        self._movement()
        self._check_view_direction()
        self._check_attack()
        self._check_curr_animation()
        self._animate()
