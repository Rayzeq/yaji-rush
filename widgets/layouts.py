from enum import Enum, auto
from typing import List

from . import Widget


class Direction(Enum):
    Vertical = auto()
    Horizontal = auto()


class ListLayout(Widget):
    def __init__(self, x: int, y: int, *widgets: List[Widget], spacing: int = 77, direction: Direction = Direction.Vertical):
        super().__init__(x, y)
        self.widgets = []
        self.spacing = spacing
        self.direction = direction

        for widget in widgets:
            self.add(widget)

    def add(self, widget: List[Widget]):
        if self.direction is Direction.Vertical:
            widget.x = self.x
            widget.y = self.y + self.spacing * len(self.widgets)
        else:
            widget.x = self.x + self.spacing * len(self.widgets)
            widget.y = self.y

        self.widgets.append(widget)
        return self

    def focus(self, index: int):
        """Focus the index-th element of this layout. Use only if elements are `Focusable`s."""
        self.unfocus()
        self.widgets[index].focus()

    def unfocus(self):
        """Unfocus every elements of this layout. Use only if elements are `Focusable`s."""
        for widget in self.widgets:
            widget.unfocus()

    def event(self, event):
        for widget in self.widgets:
            if widget.focused:
                if not widget.event(event):
                    return False

        return super().event(event)

    def draw(self, surface):
        for widget in self.widgets:
            widget.draw(surface)
