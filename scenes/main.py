from assets import ASSETS
from widgets.cog import Cog
from widgets.menu import Menu
from widgets.title import MainTitle

from . import Scene
from .game2p import Game2p


class Main(Scene):
    def __init__(self):
        super().__init__(ASSETS.image.background)

        self.menu = Menu(-10, 275) \
            .add("Solo", onclick=lambda _: (self.manager.goto("menu1p"))) \
            .add("Duel", onclick=lambda _: self.manager.goto(Game2p())) \
            .add("Settings", onclick=lambda _: self.manager.goto("settings")) \
            .add("Quit", onclick=self.back)
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

    def event(self, event):
        if self.menu.event(event):
            return super().event(event)
        return False
