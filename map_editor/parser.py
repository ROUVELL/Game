import pygame as pg
from pygame import Vector2 as vec
from config import Config

import json
import os


class _Object:
    def __init__(self, img: pg.Surface, **config):
        self.name = config['name']
        # Зберігаємо оригінальну картинку для коректного маштабування
        self._orig_image = img.convert_alpha() if config['alpha'] else img.convert()
        self._orig_rect = img.get_rect(center=config['pos'])
        #################
        self.type = config['type']
        self.alpha = config['alpha']
        self.zindex = config['zindex']
        self._get_image_and_rect(config['size'], config['pos'])

    def _get_image_and_rect(self, size: tuple, pos: tuple):
        # Після маштабування потрібно оновлювати картинку і позицію
        self.image = pg.transform.scale(self._orig_image, size)
        self.rect = self.image.get_rect(center=pos)  # Щоб розтягувати в якусь одну сторону не міняючи позиції

    def get_parr(self, origin: vec) -> dict:
        pos = list(vec(self.rect.center) - origin)
        return {
            'type': self.type,
            'name': self.name,
            'size': self.rect.size,
            'pos': pos,
            'alpha': self.alpha,
            'zindex': self.zindex
        }


class Parser:
    def __init__(self, engine):
        self._engine = engine
        self.cached_images = dict()
        self.current_world = []
        self.origin = vec(Config.CENTER)
        self._cache_images()
        self.parse_world()

    def _cache_images(self):
        # Кешуємо всі статичні картинки
        for name in os.listdir(Config.STATIC): self.cached_images[name] = pg.image.load(Config.STATIC + name)

    def _sort_world(self):
        # Сортування по z індексу
        self.current_world = sorted(self.current_world, key=lambda obj: obj.zindex)

    def parse_world(self, path: str = Config.CURRENT_MAP):
        # Відкриваємо вибрану карту, зберігаємо кожен тайл і відсортовуємо
        with open(path) as map_:
            world = json.load(map_)
            for obj in world:
                img = self.cached_images[obj['name']]
                obj['pos'] = vec(obj['pos']) + self.origin
                self.current_world.append(_Object(img, **obj))
        self._sort_world()

    def get_collided_rect(self) -> _Object | None:
        # Повертає об'ект на який наведена мишка
        x, y = pg.mouse.get_pos()
        tiles = self.current_world[::-1]
        for tile in tiles:
            if tile.rect.collidepoint(x, y): return tile

    def offset(self, dx: int, dy: int):
        # Зміна позиції всіх тайлів
        self.origin.x += int(dx)
        self.origin.y += int(dy)
        [obj.rect.move_ip(dx, dy) for obj in self.current_world]

    def add_to_world(self, img: pg.Surface, config: dict):
        # Додавання новога тайла до світу. Пересортувати для правильного відображення
        self.current_world.append(_Object(img, **config))
        self._sort_world()

    def delete_from_world(self, pos: tuple, all_: bool = False):
        # Видалення одного або всіх тайлів по позиції
        # Перевертаємо список щоб спочатку видялялися верхні
        for tile in self.current_world[::-1]:
            if tile.rect.collidepoint(pos):
                self.current_world.remove(tile)
                if not all_: return

    def save_world(self):
        # Збереження світу
        with open(Config.CURRENT_MAP, 'w', encoding='utf-8') as map_:
            map_.write(json.dumps([tile.get_parr(self.origin) for tile in self.current_world], indent=2))
