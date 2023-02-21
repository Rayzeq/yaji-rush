from typing import Dict, Any, List
import pygame

from . import Focusable
from .layouts import ListLayout, Direction
from .buttons import ButtonBase, Button, CheckButton, ListButton, ControlButton


def rindex(lst, val, start=None):
    if start is None:
        start = len(lst)-1
    for i in range(start, -1, -1):
        if lst[i] == val:
            return i
    raise ValueError


class Menu(Focusable, ListLayout):
    focused = True
    key_before: int
    key_after: int
    _selected = 0
    hidden: List[bool]

    @property
    def selected(self) -> int:
        return self._selected

    @selected.setter
    def selected(self, value: int):
        self.widgets[self._selected].unfocus()
        self._selected = value
        if self.focused:
            self.widgets[self._selected].focus()

    def __init__(self, x: int, y: int, *, direction: Direction = Direction.Vertical, **kwargs):
        super().__init__(x, y, direction=direction, **kwargs)
        if direction == Direction.Vertical:
            self.key_before = pygame.K_UP
            self.key_after = pygame.K_DOWN
        else:
            self.key_before = pygame.K_LEFT
            self.key_after = pygame.K_RIGHT
        self.hidden = []

    def _add(self, button: ButtonBase, *, hidden: bool = False, **kwargs):
        if not self.widgets:
            button.focus()
        super().add(button, **kwargs)
        self.hidden.append(hidden)

    def add(self, text: str, *, hidden: bool = False, **kwargs):
        self._add(Button(0, 0, text, **kwargs), hidden=hidden)
        return self

    def add_check(self, text: str, *, hidden: bool = False, **kwargs):
        self._add(CheckButton(0, 0, text, **kwargs), hidden=hidden)
        return self

    def add_list(self, options: Dict[str, Any], *, hidden: bool = False, **kwargs):
        self._add(ListButton(0, 0, options, **kwargs), hidden=hidden)
        return self

    def add_control(self, image: pygame.Surface, *, hidden: bool = False, **kwargs):
        self._add(ControlButton(0, 0, image, **kwargs), hidden=hidden)
        return self

    def focus(self):
        super().focus()
        self.widgets[self._selected].focus()

    def unfocus(self):
        super().unfocus()
        self.widgets[self._selected].unfocus()

    def event(self, event: pygame.event.Event):
        if super().event(event):
            if event.type == pygame.KEYDOWN:
                try:
                    if event.key == self.key_before and self._selected > 0:
                        new_index = rindex(self.hidden, False, self.selected-1)
                    elif event.key == self.key_after and self._selected < len(self.widgets) - 1:
                        new_index = self.hidden.index(False, self.selected+1)
                    else:
                        raise ValueError
                except ValueError:
                    pass
                else:
                    self.selected = new_index
                    return False

            return True

    def draw(self, surface: pygame.Surface):
        for hidden, widget in zip(self.hidden, self.widgets):
            if not hidden:
                widget.draw(surface)
