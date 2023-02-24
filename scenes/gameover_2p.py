from assets import ASSETS
from widgets.layouts import ListLayout
from widgets.box import Title, Box, Side

from . import Scene


class GameOver2p(Scene):
    def __init__(self, winner, score1, score2):
        background = ASSETS.image.background.copy()
        title = Title(0, 73, "Game Over", color=(196, 30, 30))
        title.x = (576 / 2) - (title.image.get_rect().width / 2)
        title.draw(background)

        scores = ListLayout(51, 217, spacing=120) \
            .add(Box(0, 0, f"Player 1: {score1}", side=Side.Right, width=525)) \
            .add(Box(0, 0, f"Player 2: {score2}", side=Side.Right, width=525))
        scores.draw(background)

        if winner == "tie":
            winner = ASSETS.font.PrimaSansBold[30].render(
                "Tied !", True, (250, 250, 0))
        elif winner == "player1":
            winner = ASSETS.font.PrimaSansBold[30].render(
                "Player 1 won !", True, (250, 250, 0))
        else:
            winner = ASSETS.font.PrimaSansBold[30].render(
                "Player 2 won !", True, (250, 250, 0))
        winner_x = (576 / 2) - (winner.get_rect().width / 2)
        background.blit(winner, (winner_x, 150))

        quit_box = Box(0, 505, "Press Escape", width=285)
        quit_box.x = (576 / 2) - (quit_box.image.get_rect().width / 2)
        quit_box.draw(background)

        super().__init__(background)

    def back(self):
        self.manager.goto("main", reset=True)
