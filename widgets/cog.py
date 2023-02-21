import pygame

from assets import ASSETS
from . import Widget, Animated


class Cog(Animated, Widget):
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
        self.image = pygame.transform.scale(ASSETS.image.cog, (576, 576))
        super().__init__(x, y)

        self.angle = 0

    def tick(self, _):
        self.angle += 0.4

    def draw(self, surface: pygame.Surface):
        rotated = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated.get_rect(center=self.center)
        surface.blit(rotated, rotated_rect)
