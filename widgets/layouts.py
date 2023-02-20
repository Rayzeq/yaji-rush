from enum import Enum, auto
from . import Widget


class Direction(Enum):
    Vertical = auto()
    Horizontal = auto()


class ListLayout(Widget):
    def __init__(self, x: int, y: int, *widgets, spacing: int = 77, direction: Direction = Direction.Vertical):
        super().__init__(x, y)
        self.widgets = widgets
        self.spacing = spacing
        self.direction = direction

        for i, widget in enumerate(widgets):
            if direction is Direction.Vertical:
                widget.x = x
                widget.y = y + spacing * i
            else:
                widget.x = x + spacing * i
                widget.y = y

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
                widget.event(event)

    def draw(self, surface):
        for widget in self.widgets:
            widget.draw(surface)
