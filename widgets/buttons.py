from __future__ import annotations
from typing import Dict, Any, List, Optional, Callable
from abc import abstractmethod
from functools import partial

import pygame

from . import Widget, Focusable, Clickable, Placeholder
from .box import Box, Side
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
            return False

        return super().event(event)


class Button(ButtonBase):
    def __init__(self, x: int, y: int, text: str, *, gen_args: List[Any] = [], **kwargs):
        super().__init__(x, y, gen_args=gen_args + [text], **kwargs)

    def _generate_image(self, text: str, *, focused: bool) -> pygame.Surface:
        image = self._build_image(text, scale_factor=(
            self.scale_factor + 1) if focused else None)

        if not focused:
            self.width, self.height = image.get_size()

        return image

    @staticmethod
    def _build_image(text: str, *, scale_factor: Optional[float] = None, checked: bool = False) -> pygame.Surface:
        image = Box._generate_image(
            text, side=Side.Left,
            width=285, enabled=checked
        )
        img_rect = image.get_rect()

        if scale_factor is not None:
            image = pygame.transform.smoothscale(
                image, (int(img_rect.width*scale_factor), int(img_rect.height*scale_factor)))

        return image


class CheckButton(Button):
    checked: bool = False
    ontoggle: Optional[Callable[[CheckButton, bool]]] = None

    def __init__(
        self,
        x: int, y: int, text: str, *,
        attributes: Dict[str, List[Any]] = {},
        ontoggle: Optional[Callable[[CheckButton, bool]]] = None,
        **kwargs
    ):
        super().__init__(x, y, text, attributes=dict(
            checked=[True, False], **attributes), **kwargs)
        self.ontoggle = ontoggle

    def _generate_image(self, text: str, *, focused: bool, checked: bool) -> pygame.Surface:
        image = self._build_image(
            text, checked=checked,
            scale_factor=(self.scale_factor + 1) if focused else None
        )

        if not focused:
            self.width, self.height = image.get_size()

        return image

    def click(self):
        self.checked = not self.checked
        if self.ontoggle is not None:
            self.ontoggle(self, self.checked)
        super().click()


class ListButton(ButtonBase):
    scale_factor = +0.25
    options: List[Any]
    index: int = 0
    onchange: Optional[Callable[[ListButton, Any]]] = None

    def __init__(
        self, x: int, y: int,
        options: Dict[str, Any], *,
        attributes: Dict[str, List[Any]] = {},
        onchange: Optional[Callable[[ListButton, Any]]] = None,
        **kwargs
    ):
        super().__init__(x, y, gen_args=[list(options.keys())], attributes=dict(
            index=range(len(options)), **attributes), **kwargs)
        self.options = list(options.values())
        self.onchange = onchange

    def _generate_image(self, options: List[str], *, index: int, focused: bool) -> pygame.Surface:
        image = self._build_image(
            options[index], scale_factor=(self.scale_factor + 1) if focused else None, width=186)

        if not focused:
            self.width, self.height = image.get_size()

        return image

    @staticmethod
    def _build_image(text: str, *, scale_factor: Optional[float] = None, **kwargs) -> pygame.Surface:
        image = Box._generate_image(text, **kwargs)
        img_rect = image.get_rect()

        if scale_factor is not None:
            image = pygame.transform.smoothscale(
                image, (int(img_rect.width*scale_factor), int(img_rect.height*scale_factor)))

        return image

    @property
    def value(self):
        return self.options[self.index]

    def click(self):
        super().click()
        self.next()

    def previous(self):
        self.index = (self.index - 1) % len(self.options)
        if self.onchange is not None:
            self.onchange(self, self.value)

    def set(self, index: int):
        self.index = index % len(self.options)
        if self.onchange is not None:
            self.onchange(self, self.value)

    def next(self):
        self.index = (self.index + 1) % len(self.options)
        if self.onchange is not None:
            self.onchange(self, self.value)


class ControlButton(ButtonBase):
    checked: bool = False
    onchange: Optional[Callable[[ControlButton, int]]] = None

    def __init__(
            self, x: int, y: int,
            image: pygame.Surface, *,
            gen_args: List[Any] = [],
            attributes: Dict[str, List[Any]] = {},
            onchange: Optional[Callable[[ControlButton, int]]] = None,
            offsetx: int = 0,
            **kwargs):
        super().__init__(x, y, gen_args=gen_args + [image, offsetx], attributes=dict(
            checked=[True, False], **attributes), **kwargs)
        self.onchange = onchange

    def _generate_image(self, image: pygame.Surface, offsetx: int, *, focused: bool, checked: bool) -> pygame.Surface:
        image = self._build_image(
            image, scale_factor=(self.scale_factor + 1) if focused else None, offsetx=offsetx, width=90, enabled=checked)

        if not focused:
            self.width, self.height = image.get_size()

        return image

    @staticmethod
    def _build_image(image: pygame.Surface, *, scale_factor: Optional[float] = None, offsetx: int = 0, **kwargs) -> pygame.Surface:
        image = Box._generate_image(image, offsetx=offsetx, **kwargs)
        img_rect = image.get_rect()

        if scale_factor is not None:
            image = pygame.transform.smoothscale(
                image, (int(img_rect.width*scale_factor), int(img_rect.height*scale_factor)))

        return image

    def click(self):
        self.checked = not self.checked
        super().click()

    def event(self, event):
        if self.checked and event.type == pygame.KEYDOWN:
            if self.onchange is not None:
                self.onchange(self, event.key)
            self.checked = False
            return False

        return super().event(event)
