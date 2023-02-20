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

    def __init__(self, x: int, y: int, *args, **kwargs):
        self.x = x
        self.y = y

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass

    def event(self, event: pygame.event.Event):
        pass


class Focusable(ABC):
    focused: bool = False

    def focus(self):
        self.focused = True

    def unfocus(self):
        self.focused = False


class Clickable(ABC):
    callback: Optional[Callable] = None

    def __init__(self, *args, callback: Optional[Callable] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

    def click(self):
        if self.callback is not None:
            self.callback()
