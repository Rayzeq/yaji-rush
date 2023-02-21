import pygame

from assets import ASSETS
from . import Widget, Animated


class MainTitle(Animated, Widget):
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value

        img_rect = self.image.get_rect()
        img_rect.x = value
        img_rect.y = self.y

        self.center = img_rect.center

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value

        img_rect = self.image.get_rect()
        img_rect.x = self.x
        img_rect.y = value

        self.center = img_rect.center

    def __init__(self, x: int, y: int):
        self._x, self._y = 0, 0
        self.image = ASSETS.image.title
        super().__init__(x, y)
        self.angle = -30
        self.direction = -1

    def tick(self, _):
        if abs(self.angle) > 30:
            self.direction = -self.direction

        self.angle += self.direction

    def draw(self, surface: pygame.Surface):
        rotated = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated.get_rect(center=self.center)
        surface.blit(rotated, rotated_rect)
