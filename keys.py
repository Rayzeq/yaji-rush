import pygame
from os import path

def get_file(name):
    return path.join(path.dirname(path.realpath(__file__)), name)

class Keys(pygame.sprite.Sprite):

    def __init__(self, n, x, y, j, game):
        super().__init__()
        self.n=n
        self.game = game
        self.j=j
        if self.n == 1:
            self.image = pygame.image.load(get_file('assets/q2.png'))
            self.k = "q"
        if self.n == 2:
            self.image = pygame.image.load(get_file('assets/z2.png'))
            self.k = "z"
        if self.n == 3:
            self.image = pygame.image.load(get_file('assets/s2.png'))
            self.k = "s"
        if self.n == 4:
            self.image = pygame.image.load(get_file('assets/d2.png'))
            self.k = "d"
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def remove(self):
        if self.j==1:
            self.game.all_keys1.remove(self)
        else:
            self.game.all_keys2.remove(self)

    def avance(self):
        if self.rect.y == 432:
            self.remove()
        else:
            self.rect.y += 48
