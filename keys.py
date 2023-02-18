import pygame

from assets import Assets


class Keys(pygame.sprite.Sprite):

    def __init__(self, n, x, y, j, game):
        super().__init__()
        self.n = n
        self.game = game
        self.j = j
        if self.n == 1:
            self.image = Assets.image.q2
            self.k = "q"
        if self.n == 2:
            self.image = Assets.image.z2
            self.k = "z"
        if self.n == 3:
            self.image = Assets.image.s2
            self.k = "s"
        if self.n == 4:
            self.image = Assets.image.d2
            self.k = "d"
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def remove(self):
        if self.j == 1:
            self.game.all_keys1.remove(self)
        else:
            self.game.all_keys2.remove(self)

    def avance(self):
        if self.rect.y == 432:
            self.remove()
        else:
            self.rect.y += 48
