import pygame

from assets import Assets


class Arrow(pygame.sprite.Sprite):

    def __init__(self, n, x, y, j, game):
        super().__init__()
        self.n = n
        self.j = j
        self.game = game
        if self.n == 'q':
            self.image = Assets.image.q
        if self.n == 'z':
            self.image = Assets.image.z
        if self.n == 'd':
            self.image = Assets.image.d
        if self.n == 's':
            self.image = Assets.image.s
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def remove(self):
        self.game.arrows.remove(self)

    def pressed(self):
        self.is_pressed = True
        if self.n == 'q':
            self.image = Assets.image.q2
            self.image = pygame.transform.scale(self.image, (48, 48))
        if self.n == 'z':
            self.image = Assets.image.z2
            self.image = pygame.transform.scale(self.image, (48, 48))
        if self.n == 'd':
            self.image = Assets.image.d2
            self.image = pygame.transform.scale(self.image, (48, 48))
        if self.n == 's':
            self.image = Assets.image.s2
            self.image = pygame.transform.scale(self.image, (48, 48))

    def unpressed(self):
        self.is_pressed = False
        if self.n == 'q':
            self.image = Assets.image.q
            self.image = pygame.transform.scale(self.image, (48, 48))
        if self.n == 'z':
            self.image = Assets.image.z
            self.image = pygame.transform.scale(self.image, (48, 48))
        if self.n == 'd':
            self.image = Assets.image.d
            self.image = pygame.transform.scale(self.image, (48, 48))
        if self.n == 's':
            self.image = Assets.image.s
            self.image = pygame.transform.scale(self.image, (48, 48))
