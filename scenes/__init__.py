import pygame


class Scene:
    background: pygame.Surface
    animated: list

    def __init__(self, background: pygame.Surface):
        self.background = background

    def draw(self, surface: pygame.Surface):
        surface.blit(self.background, (0, 0))

    def event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.back()
            return False
        return True


from .main import Main  # noqa (do not move)
from .one_player_menu import OnePlayerMenu  # noqa
from .settings import Settings  # noqa
from .control_settings import ControlSettings  # noqa
from .highscore import Highscore  # noqa
