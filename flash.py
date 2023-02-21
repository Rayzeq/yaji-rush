import pygame

from assets import ASSETS


class Title(pygame.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()
        self.image = ASSETS.image.flash
