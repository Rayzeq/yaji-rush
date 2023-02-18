import io
from abc import ABC, abstractmethod
from typing import Dict, Any

import pygame
from assets import Assets


class Widget(ABC):
    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass


class Header(Widget):
    def __init__(self, x: int, y: int, text: str):
        super().__init__()

        text = Assets.font.PrimaSansBold[25].render(
            text, True, (255, 255, 255))
        txt_rect = text.get_rect()

        svg_image = io.BytesIO(
            Assets.template.header.get(width=txt_rect.width*2 + 50).encode())
        self.image = pygame.image.load(svg_image).convert_alpha()
        self.rect = self.image.get_rect()
        txt_rect.centerx = self.rect.centerx
        txt_rect.centery = self.rect.centery - 3

        self.image.blit(text, txt_rect)
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Button(Widget):
    def __init__(self, x: int, y: int, text: str):
        super().__init__()

        self.x = x
        self.y = y
        self.selected = False

        self.image, self.upscaled_image = self._build_images(
            Assets.image.button, text)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.upscaled_rect = self.upscaled_image.get_rect()
        self.upscaled_rect.x = self.x - (self.upscaled_rect.width // 6)
        self.upscaled_rect.centery = self.rect.centery

    def _build_images(self, base, text, align="right", scale_factor=1.5):
        image = base.copy()
        text = Assets.font.PrimaSansBold[25].render(
            text, True, (255, 255, 255))

        img_rect = image.get_rect()
        txt_rect = text.get_rect()
        txt_rect.centery = img_rect.centery - 3
        if align == "right":
            txt_rect.right = img_rect.right - 45
        elif align == "center":
            txt_rect.centerx = img_rect.centerx
        else:
            raise ValueError(f"Invalid text alignement: {align}")

        image.blit(text, txt_rect)
        upscaled_image = pygame.transform.smoothscale(
            image, (int(img_rect.width*scale_factor), int(img_rect.height*scale_factor)))

        return image, upscaled_image

    def draw(self, surface):
        if self.selected:
            surface.blit(self.upscaled_image, self.upscaled_rect)
        else:
            surface.blit(self.image, self.rect)

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False


class CheckButton(Button):
    def __init__(self, x: int, y: int, text: str):
        super().__init__(x, y, text)

        self.checked = False

        self.checked_image, self.upscaled_checked_image = self._build_images(
            Assets.image.checked_button, text)

    def draw(self, surface):
        if self.selected:
            if self.checked:
                surface.blit(self.upscaled_checked_image, self.upscaled_rect)
            else:
                surface.blit(self.upscaled_image, self.upscaled_rect)
        else:
            if self.checked:
                surface.blit(self.checked_image, self.rect)
            else:
                surface.blit(self.image, self.rect)

    def check(self):
        self.checked = True

    def uncheck(self):
        self.checked = False

    def toggle(self):
        self.checked = not self.checked


class ListButton(Button):
    def __init__(self, x: int, y: int, options: Dict[str, Any]):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.index = 0
        self.values = list(options.values())

        self.images = [self._build_images(
            Assets.image.list_button, text, align="center", scale_factor=1.25) for text in options.keys()]
        self.rect = self.images[0][0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.upscaled_rect = self.images[0][1].get_rect()
        self.upscaled_rect.center = self.rect.center

    def draw(self, surface):
        if self.selected:
            surface.blit(self.images[self.index][1], self.upscaled_rect)
        else:
            surface.blit(self.images[self.index][0], self.rect)

    @property
    def value(self):
        return self.values[self.index]

    def previous(self):
        self.index = (self.index - 1) % len(self.images)

    def set(self, index: int):
        self.index = index % len(self.images)

    def next(self):
        self.index = (self.index + 1) % len(self.images)


class OldButton(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()

        self.name = name
        self.x = x
        self.y = y

        self.image = Assets.image[name]
        self.is_int = False
        if name[-1] == '2':
            self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.n = 1
        self.gameset = {0: [10000, 30000, 60000],
                        1: [500, 1000, 2000], 2: [3, 5, 10]}

    def select(self):
        self.image = pygame.transform.scale(
            self.image, (int(self.rect.width*1.5), int(self.rect.height*1.5)))
        self.rect.x = self.x-(self.rect.width//4)
        self.rect.y = self.y-(self.rect.height//4)

    def deselect(self):
        self.image = pygame.transform.scale(
            self.image, (self.rect.width, self.rect.height))
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def int(self):
        self.image = Assets.image[self.name + '2']
        self.is_int = True

    def deint(self):
        self.image = Assets.image[self.name]
        self.is_int = False

    def next(self):
        if self.n < 3:
            self.n += 1
        else:
            self.n = 1
        self.image = Assets.image[self.name[:-1] + str(self.n)]
