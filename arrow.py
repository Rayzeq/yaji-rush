from __future__ import annotations
from typing import List
from abc import ABC
from enum import Enum
import random

import pygame

from assets import ASSETS


class Direction(Enum):
    Left = (0, 180, "#211dde")
    Up = (1, -90, "#ded71d")
    Down = (2, 90, "#1dde29")
    Right = (3, 0, "#de1d1d")


class Arrow(ABC):
    types: List[Arrow] = []

    def __init_subclass__(cls):
        cls.types.append(cls)

    @classmethod
    def get(cls):
        Type = random.choices(
            [Normal, PlusTwo, PlusThree, TimesTwo,
                DirectionTrap, ColorTrap, ColumnTrap, DoomedBySatan, GiftedByGod],
            weights=[76, 10, 4, 1, 3, 3, 2, .5, .5]  # en %
        )[0]
        direction = random.choice(list(Direction))
        return Type(direction)

    def __init__(self, direction: Direction):
        self.direction = direction

    def draw(self, surface, lane_x, y):
        surface.blit(self.image, (lane_x + self.direction.value[0] * 48, y))

    # Pre-made default functions
    def pressed(self, player, key_direction):
        if self.direction == key_direction:
            player.combo += 1
            player.score += player.combo
        else:
            self.failed(player)
        return self.direction != key_direction

    def failed(self, player):
        player.score -= 1
        player.lives -= 1
        player.combo = 0


class Normal(Arrow):
    def __init__(self, direction: Direction):
        super().__init__(direction)
        self.image = ASSETS.image.template(
            "arrow", angle=direction.value[1], color=direction.value[2])


class PlusTwo(Arrow):
    def __init__(self, direction: Direction):
        super().__init__(direction)
        font = ASSETS.font.PrimaSansBold[15]
        if direction == Direction.Left:
            self.image = ASSETS.image.template(
                "arrow", angle=180, color="#211dde")
            x, y = +3, -2
        elif direction == Direction.Up:
            self.image = ASSETS.image.template(
                "arrow", angle=-90, color="#ded71d")
            x, y = 0, 0
        elif direction == Direction.Down:
            self.image = ASSETS.image.template(
                "arrow", angle=90, color="#1dde29")
            x, y = 0, -4
        elif direction == Direction.Right:
            self.image = ASSETS.image.template(
                "arrow", angle=0, color="#de1d1d")
            x, y = -3, -2
        else:
            raise ValueError(f"Invalid direction: {direction}")

        self.image = self.image.copy()
        text = font.render("+2", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = self.image.get_rect().center
        text_rect.centerx += x
        text_rect.centery += y
        self.image.blit(text, text_rect)

    def pressed(self, player, key_direction):
        if self.direction == key_direction:
            player.combo += 2
            player.score += player.combo
        else:
            self.failed(player)
        return self.direction != key_direction


class PlusThree(Arrow):
    def __init__(self, direction: Direction):
        super().__init__(direction)
        font = ASSETS.font.PrimaSansBold[15]
        if direction == Direction.Left:
            self.image = ASSETS.image.template(
                "arrow", angle=180, color="#211dde")
            x, y = +3, -2
        elif direction == Direction.Up:
            self.image = ASSETS.image.template(
                "arrow", angle=-90, color="#ded71d")
            x, y = 0, 0
        elif direction == Direction.Down:
            self.image = ASSETS.image.template(
                "arrow", angle=90, color="#1dde29")
            x, y = 0, -4
        elif direction == Direction.Right:
            self.image = ASSETS.image.template(
                "arrow", angle=0, color="#de1d1d")
            x, y = -3, -2
        else:
            raise ValueError(f"Invalid direction: {direction}")

        self.image = self.image.copy()
        text = font.render("+3", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = self.image.get_rect().center
        text_rect.centerx += x
        text_rect.centery += y
        self.image.blit(text, text_rect)

    def pressed(self, player, key_direction):
        if self.direction == key_direction:
            player.combo += 3
            player.score += player.combo
        else:
            self.failed(player)
        return self.direction != key_direction


class TimesTwo(Arrow):
    def __init__(self, direction: Direction):
        super().__init__(direction)
        font = ASSETS.font.PrimaSansBold[15]
        if direction == Direction.Left:
            self.image = ASSETS.image.template(
                "arrow", angle=180, color="#211dde")
            x, y = +3, -2
        elif direction == Direction.Up:
            self.image = ASSETS.image.template(
                "arrow", angle=-90, color="#ded71d")
            x, y = 0, 0
        elif direction == Direction.Down:
            self.image = ASSETS.image.template(
                "arrow", angle=90, color="#1dde29")
            x, y = 0, -4
        elif direction == Direction.Right:
            self.image = ASSETS.image.template(
                "arrow", angle=0, color="#de1d1d")
            x, y = -3, -2
        else:
            raise ValueError(f"Invalid direction: {direction}")

        self.image = self.image.copy()
        text = font.render("×2", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = self.image.get_rect().center
        text_rect.centerx += x
        text_rect.centery += y
        self.image.blit(text, text_rect)

    def pressed(self, player, key_direction):
        if self.direction == key_direction:
            player.combo *= 2
        else:
            self.failed(player)
        return self.direction != key_direction


class DirectionTrap(Arrow):
    def __init__(self, direction: Direction):
        super().__init__(direction)
        fake_direction = list(Direction)
        fake_direction.remove(direction)
        fake_direction = random.choice(fake_direction)

        self.image = ASSETS.image.template(
            "arrow", angle=fake_direction.value[1], color=direction.value[2])


class ColorTrap(Arrow):
    def __init__(self, direction: Direction):
        super().__init__(direction)
        fake_direction = list(Direction)
        fake_direction.remove(direction)
        fake_direction = random.choice(fake_direction)

        self.image = ASSETS.image.template(
            "arrow", angle=direction.value[1], color=fake_direction.value[2])


class ColumnTrap(Arrow):
    def __init__(self, direction: Direction):
        super().__init__(direction)
        fake_direction = list(Direction)
        fake_direction.remove(direction)
        self.fake_direction = random.choice(fake_direction)

        self.image = ASSETS.image.template(
            "arrow", angle=direction.value[1], color=direction.value[2])

    def draw(self, surface, lane_x, y):
        surface.blit(
            self.image, (lane_x + self.fake_direction.value[0] * 48, y))


# Display name: Banned from Hell
class DoomedBySatan(Arrow):
    def __init__(self, direction: Direction):
        super().__init__(direction)
        self.image = ASSETS.image.template(
            "arrow", angle=direction.value[1], color="#000000")

    def pressed(self, player, key_direction):
        if self.direction == key_direction:
            player.doomed_by_satan = pygame.time.get_ticks() + 2000
        return False


# Display name: Going to Heaven
class GiftedByGod(Arrow):
    def __init__(self, direction: Direction):
        super().__init__(direction)
        self.image = ASSETS.image.template(
            "glowing_arrow", angle=direction.value[1], color=direction.value[2])

    def pressed(self, player, key_direction):
        if self.direction == key_direction:
            player.gifted_by_god = pygame.time.get_ticks() + 2000
        else:
            self.failed(player)
        return False

    def draw(self, surface, lane_x, y):
        surface.blit(
            self.image, (lane_x + self.direction.value[0] * 48 - 4, y - 4))
