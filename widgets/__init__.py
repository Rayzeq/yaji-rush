from __future__ import annotations
from typing import Optional, Callable
from abc import ABC, abstractmethod

import pygame


class Placeholder:
    """
    A placeholder for some attributes. If you see errors like `expected int but
    found Placeholder`, you know some attribute hasn't been set properly.
    """


class Widget(ABC):
    x: int = Placeholder()
    y: int = Placeholder()

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass

    def event(self, event: pygame.event.Event) -> bool:
        """Do something with `event` and return whether the event should continue to propagate."""
        return True


class Focusable(ABC):
    focused: bool = False

    def focus(self):
        self.focused = True

    def unfocus(self):
        self.focused = False


class Clickable(ABC):
    onclick: Optional[Callable[[Clickable]]] = None

    def __init__(self, *args, onclick: Optional[Callable[[Clickable]]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.onclick = onclick

    def click(self):
        if self.onclick is not None:
            self.onclick(self)


class Animated(ABC):
    @abstractmethod
    def tick(self, elapsed: float):
        """
        A method called frequently to animate this widget.
        `time` is the time elapsed since the last call to this function.
        """
        pass
