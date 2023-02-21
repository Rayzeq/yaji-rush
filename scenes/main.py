import pygame

from assets import ASSETS
from widgets.cog import Cog
from widgets.menu import Menu
from widgets.title import MainTitle

from . import Scene


class Main(Scene):
    def __init__(self, f1, f2, f3, f4, f5):
        self.background = ASSETS.image.background

        self.menu = Menu(-10, 275) \
            .add("1 player", onclick=f1) \
            .add("2 players", onclick=f2) \
            .add("Settings", onclick=f3) \
            .add("Quit", onclick=f4)
        self.f5 = f5
        self.title = MainTitle(0, 0)
        self.cog = Cog(288, 288)

    def tick(self, elapsed):
        self.title.tick(elapsed)
        self.cog.tick(elapsed)

    def draw(self, surface):
        super().draw(surface)
        self.cog.draw(surface)
        self.title.draw(surface)
        self.menu.draw(surface)

    def back(self):
        self.f5()

    def event(self, event):
        if self.menu.event(event):
            return super().event(event)
        return False
