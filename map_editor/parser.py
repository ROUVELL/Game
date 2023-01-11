import pygame as pg
from pygame import Vector2 as vec
from config import Config

import json
import os


class _Object:
    def __init__(self, img: pg.Surface, group: list, **config):
        self._group = group
        #################
        self.name = config['name']
        self.type = config['type']
        self.alpha = config['alpha']
        self.zindex = config['zindex']
        #################
        self.image = img.convert_alpha() if self.alpha else img.convert()
        self.rect = self.image.get_rect(center=config['pos'])

    def kill(self):
        # Видаляємо об'єкт зі світу
        self._group.remove(self)

    def get_parr(self, origin: vec) -> dict:
        # Беремо позицію відносно origin
        pos = tuple(vec(self.rect.center) - origin)
        return {
            'type': self.type,
            'name': self.name,
            'pos': pos,
            'alpha': self.alpha,
            'zindex': self.zindex
        }


class Parser:
    def __init__(self, engine):
        self._engine = engine
        ############
        self.cached_images = dict()
        self.textures = []
        self.sprites = []
        ############
        self.origin = vec(Config.CENTER)
        self.changed = False  # Чи змінили ми щось на карті
        self._cache_images()
        self.parse_world()

    def _cache_images(self):
        # Кешуємо всі статичні картинки
        for name in os.listdir(Config.STATIC): self.cached_images[name] = pg.image.load(Config.STATIC + name)

    def parse_world(self, path: str = Config.CURRENT_MAP):
        # Відкриваємо вибрану карту, зберігаємо кожен тайл і відсортовуємо
        with open(path) as map_:
            world = json.load(map_)
            for obj in world:
                img = self.cached_images[obj['name']]
                obj['pos'] = vec(obj['pos']) + self.origin
                match obj['type']:
                    case 'texture': self.textures.append(_Object(img, self.textures, **obj))
                    case 'sprite': self.sprites.append(_Object(img, self.sprites, **obj))

        self.textures.sort(key=lambda obj: obj.zindex)
        self.sprites.sort(key=lambda obj: obj.zindex)
        self.changed = False

    def get_world(self) -> list[_Object]:
        # Повертає копію світу
        return [*self.textures, *self.sprites]

    def get_collided_obj(self) -> _Object | None:
        # Повертає об'ект на який наведена мишка
        x, y = pg.mouse.get_pos()
        tiles = self.get_world()[::-1]
        for tile in tiles:
            if tile.rect.collidepoint(x, y): return tile

    def offset(self, ofsset: pg.Vector2):
        # Зміна позиції всіх тайлів
        self.origin.x += ofsset.x
        self.origin.y += ofsset.y
        [obj.rect.move_ip(ofsset) for obj in self.get_world()]

    def restore_world(self):
        # Відновлюмо світ якщо щось змінили
        if self.changed:
            self.textures = []
            self.sprites = []
            self.parse_world()

    def add_to_world(self, **config):
        # Додавання новога об'єкта до світу. Пересортувати для правильного відображення
        img = self.cached_images[config['name']]
        match config['type']:
            case 'texture':
                self.textures.append(_Object(img, self.textures, **config))
                self.textures.sort(key=lambda obj: obj.zindex)
            case 'sprite':
                self.sprites.append(_Object(img, self.sprites, **config))
                self.sprites.sort(key=lambda obj: obj.zindex)
        self.changed = True

    def delete_collided_obj(self, pos: tuple[int | int], all_: bool = False):
        # Видалення одного або всіх об'єктів по позиції
        # Перевертаємо список щоб спочатку видялялися верхні
        for tile in sorted(self.get_world(), key=lambda obj: obj.zindex):
            if tile.rect.collidepoint(pos):
                self.changed = True
                tile.kill()
                if not all_: break

    def save_world(self):
        # Збереження світу
        if self.changed:
            with open(Config.CURRENT_MAP, 'w', encoding='utf-8') as map_:
                map_.write(json.dumps([tile.get_parr(self.origin) for tile in self.get_world()], indent=2))
        self.changed = False
