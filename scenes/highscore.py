import pygame

from saves import SAVES
from assets import ASSETS
from widgets.cog import Cog
from widgets.layouts import ListLayout
from widgets.box import Title, Box, Side

from . import Scene


class Highscore(Scene):
    def __init__(self, f1):
        self.background = ASSETS.image.background
        self.cog = Cog(0, 0)
        self.f1 = f1

    def refresh(self):
        self.foreground = pygame.Surface((576, 576), pygame.SRCALPHA)
        title = Title(0, 73, "High Scores")
        title.x = (576 / 2) - (title.image.get_rect().width / 2)
        title.draw(self.foreground)

        time = SAVES.time
        score = SAVES.score
        lives = SAVES.lives
        time = 'N/A' if time is None else f'{time[1]} by {time[0]}'
        score = 'N/A' if score is None else f'{score[1]}s by {score[0]}'
        lives = 'N/A' if lives is None else f'{lives[1]} by {lives[0]}'

        scores = ListLayout(51, 193, spacing=96) \
            .add(Box(0, 0, f"Time: {time}", side=Side.Right, width=525)) \
            .add(Box(0, 0, f"Score: {score}", side=Side.Right, width=525)) \
            .add(Box(0, 0, f"Lives: {lives}", side=Side.Right, width=525))
        scores.draw(self.foreground)

        quit_box = Box(0, 505, "Press Escape")
        quit_box.x = (576 / 2) - (quit_box.image.get_rect().width / 2)
        quit_box.draw(self.foreground)

    def tick(self, elapsed):
        self.cog.tick(elapsed)

    def draw(self, surface):
        super().draw(surface)
        self.cog.draw(surface)
        surface.blit(self.foreground, (0, 0))

    def back(self):
        self.f1()
