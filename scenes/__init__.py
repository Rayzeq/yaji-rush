from __future__ import annotations
import pygame


class Scene:
    background: pygame.Surface
    animated: list
    manager: SceneManager

    def __init__(self, background: pygame.Surface):
        self.background = background

    def tick(self, elapsed):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.background, (0, 0))

    def back(self, *_, **__):
        self.manager.back()

    def event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.back()
            return False
        return True


class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current = None
        self.history = []
        self.running = True

    def add(self, name, scene):
        self.scenes[name] = scene
        scene.manager = self

    def goto(self, scene, reset=False):
        self.history.append(self.current)
        if isinstance(scene, Scene):
            self.current = scene
            scene.manager = self
        elif isinstance(scene, str):
            self.current = self.scenes[scene]
        else:
            raise ValueError(f"Invalid scene: {scene}")

        if reset:
            self.history = [None]

    def back(self):
        self.current = self.history.pop()
        if self.current is None:
            self.running = False

    def tick(self, elapsed):
        self.current.tick(elapsed)

    def draw(self, surface: pygame.Surface):
        self.current.draw(surface)

    def event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.running = False

        self.current.event(event)


from .main import Main  # noqa (do not move)
from .one_player_menu import OnePlayerMenu  # noqa
from .settings import Settings  # noqa
from .control_settings import ControlSettings  # noqa
