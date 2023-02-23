from __future__ import annotations
from typing import List
from abc import ABC
from enum import Enum
import random

from assets import ASSETS


class Direction(Enum):
    Left = 0
    Up = 1
    Down = 2
    Right = 3


class Arrow(ABC):
    types: List[Arrow] = []

    def __init_subclass__(cls):
        cls.types.append(cls)

    @classmethod
    def get(cls):
        direction = random.choice(list(Direction))
        return Normal(direction)

    def __init__(self, direction: Direction):
        self.direction = direction

    def draw(self, surface, lane_x, y):
        surface.blit(self.image, (lane_x + self.direction.value * 48, y))


class Normal(Arrow):
    def __init__(self, direction: Direction):
        super().__init__(direction)
        if direction == Direction.Left:
            self.image = ASSETS.image.template(
                "arrow", angle=180, color="#211dde")
        elif direction == Direction.Up:
            self.image = ASSETS.image.template(
                "arrow", angle=-90, color="#ded71d")
        elif direction == Direction.Down:
            self.image = ASSETS.image.template(
                "arrow", angle=90, color="#1dde29")
        elif direction == Direction.Right:
            self.image = ASSETS.image.template(
                "arrow", angle=0, color="#de1d1d")
        else:
            raise ValueError(f"Invalid direction: {direction}")

    def pressed(self, player, key_direction):
        if self.direction == key_direction:
            player.score += player.combo + 1
            player.combo += 1
        else:
            player.score -= 1
            player.lives -= 1
            player.combo = 0
        return self.direction != key_direction
