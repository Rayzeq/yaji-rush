from typing import Dict, Any, List, Tuple
from abc import abstractmethod
from functools import partial

import pygame

from assets import Assets
from . import Widget, Focusable, Clickable, Placeholder
from .box import Box
from .utils import PropertyMatrix


class ButtonBase(Clickable, Focusable, Widget):
    # Scale factor when the button is focused
    scale_factor: float = +0.5

    attributes: List[str]
    images: PropertyMatrix
    width: int = Placeholder()
    height: int = Placeholder()

    @property
    def focused_x(self) -> int:
        return self.x - (self.width * self.scale_factor) // 2

    @property
    def focused_y(self) -> int:
        return self.y - (self.height * self.scale_factor) // 2

    def __init__(self, x: int, y: int, *, gen_args: list = [], attributes: Dict[str, List[Any]] = {}, **kwargs):
        super().__init__(x, y, **kwargs)

        attributes = dict(focused=(True, False), **attributes)
        self.attributes = tuple(attributes.keys())
        self.images = PropertyMatrix(
            partial(self._generate_image, *gen_args), **attributes)

    @abstractmethod
    def _generate_image(self, **kwargs) -> pygame.Surface:
        pass

    def draw(self, surface: pygame.Surface):
        image = self.images.get(**{name: getattr(self, name)
                                   for name in self.attributes})
        if self.focused:
            surface.blit(image, (self.focused_x, self.focused_y))
        else:
            surface.blit(image, (self.x, self.y))

    def event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.click()


class Button(ButtonBase):
    def __init__(self, x: int, y: int, text: str, *, gen_args: List[Any] = [], **kwargs):
        super().__init__(x, y, gen_args=gen_args + [text], **kwargs)

    def _generate_image(self, text: str, *, focused: bool) -> pygame.Surface:
        image = self._build_image(
            Assets.image.button, text, scale_factor=1.5 if focused else 0.0)

        if not focused:
            self.width, self.height = image.get_size()

        return image

    def _build_image(self, base: pygame.Surface, text: str, align: str = "right", scale_factor: float = 0.0) -> pygame.Surface:
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

        if scale_factor:
            image = pygame.transform.smoothscale(
                image, (int(img_rect.width*scale_factor), int(img_rect.height*scale_factor)))

        return image


class CheckButton(Button):
    checked: bool = False

    def __init__(self, x: int, y: int, text: str, *, attributes: Dict[str, List[Any]] = {}, **kwargs):
        super().__init__(x, y, text, attributes=dict(
            checked=[True, False], **attributes), **kwargs)

    def _generate_image(self, text: str, *, focused: bool, checked: bool) -> pygame.Surface:
        base = Assets.image.checked_button if checked else Assets.image.button
        image = self._build_image(
            base, text, scale_factor=1.5 if focused else 0.0)

        if not focused:
            self.width, self.height = image.get_size()

        return image

    def click(self):
        super().click()
        self.checked = not self.checked


class ListButton(ButtonBase):
    options: List[Any]
    index: int = 0

    def __init__(self, x: int, y: int, options: Dict[str, Any], *, attributes: Dict[str, List[Any]] = {}, **kwargs):
        super().__init__(x, y, gen_args=[list(options.keys())], attributes=dict(
            index=range(len(options)), **attributes), **kwargs)
        self.options = list(options.values())

    def _generate_image(self, options: List[str], *, index: int, focused: bool) -> pygame.Surface:
        image = self._build_image(
            options[index], scale_factor=1.5 if focused else 0.0, width=186)

        if not focused:
            self.width, self.height = image.get_size()

        return image

    def _build_image(self, text: str, *, scale_factor: float = 0.0, **kwargs) -> pygame.Surface:
        image = Box._generate_image(text, **kwargs)
        img_rect = image.get_rect()

        if scale_factor:
            image = pygame.transform.smoothscale(
                image, (int(img_rect.width*scale_factor), int(img_rect.height*scale_factor)))

        return image

    @property
    def value(self):
        return self.options[self.index]

    def previous(self):
        self.index = (self.index - 1) % len(self.options)

    def set(self, index: int):
        self.index = index % len(self.options)

    def next(self):
        self.index = (self.index + 1) % len(self.options)


class ControlButton(ButtonBase):
    checked: bool = False

    def __init__(
            self, x: int, y: int,
            image: pygame.Surface, *,
            gen_args: List[Any] = [],
            attributes: Dict[str, List[Any]] = {},
            offsetx: int = 0,
            **kwargs):
        super().__init__(x, y, gen_args=gen_args + [image, offsetx], attributes=dict(
            checked=[True, False], **attributes), **kwargs)

    def _generate_image(self, image: pygame.Surface, offsetx: int, *, focused: bool, checked: bool) -> pygame.Surface:
        image = self._build_image(
            image, scale_factor=1.5 if focused else 0.0, offsetx=offsetx, width=90, enabled=checked)

        if not focused:
            self.width, self.height = image.get_size()

        return image

    def _build_image(self, image: pygame.Surface, *, scale_factor: float = 0.0, offsetx: int = 0, **kwargs) -> pygame.Surface:
        image = Box._generate_image(image, offsetx=offsetx, **kwargs)
        img_rect = image.get_rect()

        if scale_factor:
            image = pygame.transform.smoothscale(
                image, (int(img_rect.width*scale_factor), int(img_rect.height*scale_factor)))

        return image

    def click(self):
        super().click()
        self.checked = not self.checked
