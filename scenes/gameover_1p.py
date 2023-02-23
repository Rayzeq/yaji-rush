from saves import SAVES
from assets import ASSETS
from widgets.layouts import ListLayout
from widgets.box import Title, Box, Side

from game import Mode
from . import Scene


class GameOver1p(Scene):
    def __init__(self, mode, score):
        background = ASSETS.image.background.copy()
        title = Title(0, 73, "Game Over", color=(196, 30, 30))
        title.x = (576 / 2) - (title.image.get_rect().width / 2)
        title.draw(background)

        if mode == Mode.Custom:
            highscore = 'N/A'
        else:
            highscore = SAVES.get(mode)
            if mode == Mode.Score:
                highscore = 'N/A' if highscore is None else f"{highscore[1]}s by {highscore[0]}"
            else:
                highscore = 'N/A' if highscore is None else f"{highscore[1]} by {highscore[0]}"

        if mode == Mode.Score:
            score = f"{score}s"

        scores = ListLayout(51, 217, spacing=120) \
            .add(Box(0, 0, f"Score:         {score}", side=Side.Right, width=525)) \
            .add(Box(0, 0, f"High score: {highscore}", side=Side.Right, width=525))
        scores.draw(background)

        quit_box = Box(0, 505, "Press Escape")
        quit_box.x = (576 / 2) - (quit_box.image.get_rect().width / 2)
        quit_box.draw(background)

        super().__init__(background)

    def back(self):
        self.manager.goto("main", reset=True)
