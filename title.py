import pygame

from assets import Assets


class Title(pygame.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = Assets.image.title
        self.image_rotated = Assets.image.title
        # self.image = pygame.transform.rotate(self.image, -30)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.angle = 0

    def zoom(self, n):
        self.image = pygame.transform.scale(
            self.image, (self.rect.width+n, self.rect.height+n))

    def animate(self):
        anim = -30
        blitRotateCenter(self.screen, self.image,
                         (self.rect.x, self.rect.y), -30)
        while anim < 60:
            blitRotateCenter(self.screen, self.image,
                             (self.rect.x, self.rect.y), 1)
            anim += 1
        while anim > 1:
            blitRotateCenter(self.screen, self.image,
                             (self.rect.x, self.rect.y), -1)

    def blitRotateCenter(self, surf, image, topleft, angle):

        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(
            center=image.get_rect(topleft=topleft).center)

        surf.blit(rotated_image, new_rect)


class Cog(pygame.sprite.Sprite):

    def __init__(self, screen, x, y):
        super().__init__()
        self.screen = screen
        self.image = Assets.image.cog
        self.image = self.image = pygame.transform.scale(
            self.image, (576, 576))
        self.image_rotated = Assets.image.cog
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = 0

    def zoom(self, n):
        self.image = pygame.transform.scale(
            self.image, (self.rect.width+n, self.rect.height+n))

    def animate(self):
        self.blitRotateCenter(self.screen, self.image,
                              (self.rect.x, self.rect.y), self.angle)
        self.angle += 0.4

    def blitRotateCenter(self, surf, image, topleft, angle):

        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(
            center=image.get_rect(topleft=topleft).center)

        surf.blit(rotated_image, new_rect)
