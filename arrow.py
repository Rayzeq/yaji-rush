import pygame
from os import path


def get_file(name):
    return path.join(path.dirname(path.realpath(__file__)), name)


class Arrow(pygame.sprite.Sprite):

    def __init__(self, n, x, y, j, game):
        super().__init__()
        self.n = n
        self.j = j
        self.game = game
        if self.n == 'q':
            self.image = pygame.image.load(get_file('assets/q.png'))
        if self.n == 'z':
            self.image = pygame.image.load(get_file('assets/z.png'))
        if self.n == 'd':
            self.image = pygame.image.load(get_file('assets/d.png'))
        if self.n == 's':
            self.image = pygame.image.load(get_file('assets/s.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def remove(self):
        self.game.arrows.remove(self)

    def pressed(self):
        self.is_pressed = True
        if self.n == 'q':
            self.image = pygame.image.load(get_file('assets/q2.png'))
            self.image = pygame.transform.scale(self.image, (48, 48))
        if self.n == 'z':
            self.image = pygame.image.load(get_file('assets/z2.png'))
            self.image = pygame.transform.scale(self.image, (48, 48))
        if self.n == 'd':
            self.image = pygame.image.load(get_file('assets/d2.png'))
            self.image = pygame.transform.scale(self.image, (48, 48))
        if self.n == 's':
            self.image = pygame.image.load(get_file('assets/s2.png'))
            self.image = pygame.transform.scale(self.image, (48, 48))

    def unpressed(self):
        self.is_pressed = False
        if self.n == 'q':
            self.image = pygame.image.load(get_file('assets/q.png'))
            self.image = pygame.transform.scale(self.image, (48, 48))
        if self.n == 'z':
            self.image = pygame.image.load(get_file('assets/z.png'))
            self.image = pygame.transform.scale(self.image, (48, 48))
        if self.n == 'd':
            self.image = pygame.image.load(get_file('assets/d.png'))
            self.image = pygame.transform.scale(self.image, (48, 48))
        if self.n == 's':
            self.image = pygame.image.load(get_file('assets/s.png'))
            self.image = pygame.transform.scale(self.image, (48, 48))
