import pygame

from assets import Assets


class Title(pygame.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()
        self.image = Assets.image.flash
