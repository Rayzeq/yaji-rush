from enum import Enum
from typing import Union, Optional, Dict, Any

import pygame

from assets import ASSETS
from . import Widget


class Side(Enum):
    Left = 0
    Center = 1
    Right = 2


class Box(Widget):
    def __init__(
        self, x: int, y: int,
        content: Union[str, pygame.Surface], *,
        base: Optional[pygame.Surface] = None,
        padding: int = 0,
        font_size: int = 25,
        font_color: pygame.Color = pygame.Color(255, 255, 255),
        side: Side = Side.Center,
        **kwargs: Dict[str, Any]
    ):
        super().__init__(x, y)
        self.image = self._generate_image(
            content, base=base, padding=padding,
            font_size=font_size, font_color=font_color,
            side=side,
            **kwargs
        )

    @staticmethod
    def _generate_image(
        content: Union[str, pygame.Surface], *,
        base: Optional[pygame.Surface] = None,
        padding: int = 0,
        font_size: int = 25,
        font_color: pygame.Color = pygame.Color(255, 255, 255),
        side: Side = Side.Center,
        offsetx: int = 0, offsety: int = 0,
        **kwargs: Dict[str, Any]
    ):
        if isinstance(content, str):
            content = ASSETS.font.PrimaSansBold[font_size].render(
                content, True, font_color)
            offsety -= 3
        elif isinstance(content, pygame.Surface):
            content = content
        else:
            raise ValueError(f"Invalid box content: {content}")

        content_bbox = content.get_rect()

        if base is None:
            if side == Side.Center:
                width = content_bbox.width + 50 * 2 + padding * 2
            else:
                width = content_bbox.width + 50 + padding
            base = ASSETS.image.template(
                "box",
                **{
                    "width": width,
                    "enabled": False,
                    "side": side.value,
                    **kwargs
                }
            )

        base = base.copy()
        base_bbox = base.get_rect()

        if side == Side.Left:
            content_bbox.right = base_bbox.right - 50 - padding + offsetx
        elif side == Side.Center:
            content_bbox.centerx = base_bbox.centerx + offsetx
        else:
            content_bbox.left = base_bbox.left + 50 + padding + offsetx
        content_bbox.centery = base_bbox.centery + offsety

        base.blit(content, content_bbox)

        return base

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.x, self.y))


class Title(Box):
    def __init__(
        self, x: int, y: int, text: str, *,
        color: pygame.Color = pygame.Color(255, 255, 255), padding: int = 10,
    ):
        super().__init__(x, y, text, font_color=color, padding=padding)
