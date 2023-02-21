import pygame

from assets import ASSETS
from widgets.cog import Cog
from widgets.menu import Menu
from widgets.box import Title

from . import Scene


class OnePlayerMenu(Scene):
    def __init__(self, f1, f2, f3, f4, f5, f6):
        self.background = ASSETS.image.background

        self.menu = Menu(-50, 110) \
            .add("Time", onclick=f1) \
            .add("Score", onclick=f2) \
            .add("Lives", onclick=f3) \
            .add("Custom", onclick=f4) \
            .add("High score", onclick=f5) \
            .add("Back", onclick=self.back)
        self.f6 = f6
        self.title = Title(0, 50, "1 player")
        self.title.x = (576 / 2) - (self.title.image.get_rect().width / 2)
        self.cogs = [
            Cog(288, -288),
            Cog(288, 288),
            Cog(-288, -288),
            Cog(-288, 288)
        ]

    def tick(self, elapsed):
        for cog in self.cogs:
            cog.tick(elapsed)

    def draw(self, surface):
        super().draw(surface)
        for cog in self.cogs:
            cog.draw(surface)
        self.title.draw(surface)
        self.menu.draw(surface)

    def back(self, button=None):
        if button is not None:
            self.menu.selected = 0
        self.f6()

    def event(self, event):
        if self.menu.event(event):
            return super().event(event)
        return False
