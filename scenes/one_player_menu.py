from game import Mode
from assets import ASSETS
from widgets.cog import Cog
from widgets.menu import Menu
from widgets.box import Title

from . import Scene
from .highscore import Highscore
from .game1p import Game1p


class OnePlayerMenu(Scene):
    def __init__(self):
        super().__init__(ASSETS.image.background)

        self.menu = Menu(-50, 110) \
            .add("Time", onclick=lambda _: self.manager.goto(Game1p(Mode.Time))) \
            .add("Score", onclick=lambda _: self.manager.goto(Game1p(Mode.Score))) \
            .add("Lives", onclick=lambda _: self.manager.goto(Game1p(Mode.Lives))) \
            .add("Custom", onclick=lambda _: self.manager.goto(Game1p(Mode.Custom))) \
            .add("High score", onclick=lambda _: self.manager.goto(Highscore())) \
            .add("Back", onclick=self.back)
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
        super().back()
        if button is not None:
            self.menu.selected = 0

    def event(self, event):
        if self.menu.event(event):
            return super().event(event)
        return False
