from functools import partial
import pygame

from assets import ASSETS
from settings import SETTINGS
from widgets.cog import Cog
from widgets.box import Title
from widgets.buttons import Button
from widgets.menu import Menu, Direction

from . import Scene


class ControlSettings(Scene):

    def __init__(self):
        self.background = ASSETS.image.background

        self.top_menu = Menu(27, 200, spacing=144, direction=Direction.Horizontal) \
            .add_control(
                ASSETS.image.template(
                    "arrow_icon", color="#211dde", angle=180),
                onchange=partial(self.set_key, 'p1', 'left')
        ) \
            .add_control(
                ASSETS.image.template(
                    "arrow_icon", color="#e2cb0e", angle=-90),
                offsetx=2, onchange=partial(self.set_key, 'p1', 'up')
        ) \
            .add_control(
                ASSETS.image.template("arrow_icon", color="#0ee20e", angle=90),
                offsetx=2, onchange=partial(self.set_key, 'p1', 'down')
        ) \
            .add_control(
                ASSETS.image.template("arrow_icon", color="#e20e0e", angle=0),
                offsetx=5, onchange=partial(self.set_key, 'p1', 'right')
        )

        self.bottom_menu = Menu(27, 354, spacing=144, direction=Direction.Horizontal) \
            .add_control(
                ASSETS.image.template(
                    "arrow_icon", color="#211dde", angle=180),
                onchange=partial(self.set_key, 'p2', 'left')
        ) \
            .add_control(
                ASSETS.image.template(
                    "arrow_icon", color="#e2cb0e", angle=-90),
                offsetx=2, onchange=partial(self.set_key, 'p2', 'up')
        ) \
            .add_control(
                ASSETS.image.template("arrow_icon", color="#0ee20e", angle=90),
                offsetx=2, onchange=partial(self.set_key, 'p2', 'down')
        ) \
            .add_control(
                ASSETS.image.template("arrow_icon", color="#e20e0e", angle=0),
                offsetx=5, onchange=partial(self.set_key, 'p2', 'right')
        )
        self.bottom_menu.unfocus()

        self.button_back = Button(-50, 500, "Back", onclick=self.back)

        self.font = ASSETS.font.PrimaSansBold[25]
        self._cache = {
            "p1": {
                "left": self.font.render(pygame.key.name(SETTINGS.p1_controls.left), True, (0, 0, 0)),
                "up": self.font.render(pygame.key.name(SETTINGS.p1_controls.up), True, (0, 0, 0)),
                "down": self.font.render(pygame.key.name(SETTINGS.p1_controls.down), True, (0, 0, 0)),
                "right": self.font.render(pygame.key.name(SETTINGS.p1_controls.right), True, (0, 0, 0)),
            },
            "p2": {
                "left": self.font.render(pygame.key.name(SETTINGS.p2_controls.left), True, (0, 0, 0)),
                "up": self.font.render(pygame.key.name(SETTINGS.p2_controls.up), True, (0, 0, 0)),
                "down": self.font.render(pygame.key.name(SETTINGS.p2_controls.down), True, (0, 0, 0)),
                "right": self.font.render(pygame.key.name(SETTINGS.p2_controls.right), True, (0, 0, 0)),
            },
        }

        self.foreground = pygame.Surface((576, 576), pygame.SRCALPHA)
        title = Title(0, 50, "Controls")
        title.x = (576 / 2) - (title.image.get_rect().width / 2)
        title.draw(self.foreground)
        self.foreground.blit(ASSETS.image.layout_ctrl_p1, (0, 152))
        self.foreground.blit(ASSETS.image.layout_ctrl_p2, (0, 306))

        self.cogs = [
            Cog(288, 0),
            Cog(-288, 0)
        ]

    def set_key(self, player, key, _, value):
        setattr(
            SETTINGS.p1_controls if player == "p1" else SETTINGS.p2_controls,
            key, value
        )
        self._cache[player][key] = self.font.render(
            pygame.key.name(value), True, (0, 0, 0))

    def tick(self, elapsed):
        for cog in self.cogs:
            cog.tick(elapsed)

    def draw(self, surface):
        super().draw(surface)
        for cog in self.cogs:
            cog.draw(surface)
        surface.blit(self.foreground, (0, 0))
        self.top_menu.draw(surface)
        self.bottom_menu.draw(surface)
        self.button_back.draw(surface)

        self.draw_key(
            surface,
            int(30 + 85 / 2), int(152 + 99 + 43 / 2) - 3,
            self._cache["p1"]["left"]
        )
        self.draw_key(
            surface,
            int(174 + 85 / 2), int(152 + 99 + 43 / 2) - 3,
            self._cache["p1"]["up"]
        )
        self.draw_key(
            surface,
            int(318 + 85 / 2), int(152 + 99 + 43 / 2) - 3,
            self._cache["p1"]["down"]
        )
        self.draw_key(
            surface,
            int(462 + 85 / 2), int(152 + 99 + 43 / 2) - 3,
            self._cache["p1"]["right"]
        )

        self.draw_key(
            surface,
            int(30 + 85 / 2), int(306 + 99 + 43 / 2) - 3,
            self._cache["p2"]["left"]
        )
        self.draw_key(
            surface,
            int(174 + 85 / 2), int(306 + 99 + 43 / 2) - 3,
            self._cache["p2"]["up"]
        )
        self.draw_key(
            surface,
            int(318 + 85 / 2), int(306 + 99 + 43 / 2) - 3,
            self._cache["p2"]["down"]
        )
        self.draw_key(
            surface,
            int(462 + 85 / 2), int(306 + 99 + 43 / 2) - 3,
            self._cache["p2"]["right"]
        )

    def draw_key(self, surface, centerx, centery, img):
        rect = img.get_rect()
        rect.center = (centerx, centery)
        surface.blit(img, rect)

    def back(self, button=None):
        super().back()
        if button is not None:
            self.top_menu.focus()
            self.button_back.unfocus()

    def event(self, event):
        if self.top_menu.focused:
            propagate = self.top_menu.event(event)
        elif self.bottom_menu.focused:
            propagate = self.bottom_menu.event(event)
        else:
            propagate = self.button_back.event(event)

        if propagate and super().event(event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.bottom_menu.focused:
                        self.top_menu.selected = self.bottom_menu.selected
                        self.top_menu.focus()
                        self.bottom_menu.unfocus()
                        return False
                    elif self.button_back.focused:
                        self.bottom_menu.focus()
                        self.button_back.unfocus()
                        return False
                elif event.key == pygame.K_DOWN:
                    if self.top_menu.focused:
                        self.bottom_menu.selected = self.top_menu.selected
                        self.bottom_menu.focus()
                        self.top_menu.unfocus()
                        return False
                    elif self.bottom_menu.focused:
                        self.button_back.focus()
                        self.bottom_menu.unfocus()
                        return False
            return True
        return False
