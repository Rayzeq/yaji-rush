import pygame

from assets import ASSETS
from settings import SETTINGS
from widgets.cog import Cog
from widgets.menu import Menu
from widgets.box import Title

from . import Scene


class Settings(Scene):
    def __init__(self):
        super().__init__(ASSETS.image.background)

        self.left_menu = Menu(-100, 200) \
            .add_check("Time", ontoggle=self.toggle_time) \
            .add_check("Score", ontoggle=self.toggle_score) \
            .add_check("Lives", ontoggle=self.toggle_lives) \
            .add("Controls", onclick=lambda _: self.manager.goto("controls")) \
            .add("Back", onclick=self.back)

        self.right_menu = Menu(288, 200) \
            .add_list({"10s": 10, "30s": 30, "60s": 60}, onchange=self.change_time, hidden=True) \
            .add_list({"500": 500, "1000": 1000, "2000": 2000}, onchange=self.change_score, hidden=True) \
            .add_list({"3": 3, "5": 5, "10": 10}, onchange=self.change_lives, hidden=True)
        self.right_menu.unfocus()

        self.title = Title(0, 50, "Settings")
        self.title.x = (576 / 2) - (self.title.image.get_rect().width / 2)
        self.cogs = [
            Cog(288, 0),
            Cog(-288, 0)
        ]

    def toggle_time(self, _, value: bool):
        self.right_menu.hidden[0] = not value
        SETTINGS.time = self.right_menu.widgets[0].value if value else None

    def toggle_score(self, _, value: bool):
        self.right_menu.hidden[1] = not value
        SETTINGS.score = self.right_menu.widgets[1].value if value else None

    def toggle_lives(self, _, value: bool):
        self.right_menu.hidden[2] = not value
        SETTINGS.lives = self.right_menu.widgets[2].value if value else None

    def change_time(self, _, value: int):
        SETTINGS.time = value

    def change_score(self, _, value: int):
        SETTINGS.score = value

    def change_lives(self, _, value: int):
        SETTINGS.lives = value

    def tick(self, elapsed):
        for cog in self.cogs:
            cog.tick(elapsed)

    def draw(self, surface):
        super().draw(surface)
        for cog in self.cogs:
            cog.draw(surface)
        self.title.draw(surface)
        self.left_menu.draw(surface)
        self.right_menu.draw(surface)

    def back(self, button=None):
        super().back()
        if button is not None:
            self.left_menu.selected = 0
            self.left_menu.focus()

    def event(self, event):
        if self.left_menu.focused:
            propagate = self.left_menu.event(event)
        else:
            propagate = self.right_menu.event(event)

        if propagate and super().event(event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.right_menu.focused:
                    self.left_menu.selected = self.right_menu.selected
                    self.left_menu.focus()
                    self.right_menu.unfocus()
                    return False
                elif event.key == pygame.K_RIGHT \
                        and self.left_menu.focused \
                        and self.left_menu.selected < 3 \
                        and not self.right_menu.hidden[self.left_menu.selected]:
                    self.right_menu.selected = self.left_menu.selected
                    self.right_menu.focus()
                    self.left_menu.unfocus()
                    return False
            return True
        return False
