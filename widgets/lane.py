import pygame
import numpy as np

import arrow
from arrow import Arrow, Direction
from assets import ASSETS
from settings import SETTINGS
from . import Widget


class PlayerLane(Widget):
    def __init__(self, x: int, player, display_lives=None):
        super().__init__(x, 0)
        self.xleft = self.x + 23
        self.xup = self.xleft + 48
        self.xdown = self.xup + 48
        self.xright = self.xdown + 48
        self.arrow_y = 432

        self.player = player
        self.flash_time = 0
        self.pressed = {
            Direction.Left: False,
            Direction.Up: False,
            Direction.Down: False,
            Direction.Right: False,
        }
        self.pressed_placeholders = {
            Direction.Left: (arrow.Normal(arrow.Direction.Left), (self.xleft, self.arrow_y)),
            Direction.Up: (arrow.Normal(arrow.Direction.Up), (self.xleft, self.arrow_y)),
            Direction.Down: (arrow.Normal(arrow.Direction.Down), (self.xleft, self.arrow_y)),
            Direction.Right: (arrow.Normal(arrow.Direction.Right), (self.xleft, self.arrow_y)),
        }

        if display_lives is None:
            self.display_lives = SETTINGS.lives is not None
        else:
            self.display_lives = display_lives

        self.doomed_cache = (0, None)

    def draw_background(self, surface, lives=None):
        surface.blit(ASSETS.image.player_lane, (self.x, 0))
        surface.blit(ASSETS.image.template(
            "arrow_placeholder", angle=180), (self.xleft - 1, self.arrow_y - 1))
        surface.blit(ASSETS.image.template(
            "arrow_placeholder", angle=-90), (self.xup - 1, self.arrow_y - 1))
        surface.blit(ASSETS.image.template(
            "arrow_placeholder", angle=90), (self.xdown - 1, self.arrow_y - 1))
        surface.blit(ASSETS.image.template(
            "arrow_placeholder", angle=-0), (self.xright - 1, self.arrow_y - 1))

        if self.display_lives:
            surface.blit(ASSETS.image.heart, (self.x + 162, 489))

    def flash(self):
        self.flash_time = pygame.time.get_ticks() + 25

    def key_pressed(self, direction):
        if not (self.player.doomed_by_satan > pygame.time.get_ticks()):
            failed = self.player.arrows[-1].pressed(self.player, direction)
            if not failed:
                if self.player.gifted_by_god > pygame.time.get_ticks():
                    self.player.score += self.player.combo
                self.player.arrows.pop()
                self.player.arrows.insert(0, Arrow.get())
            else:
                self.flash()

    def draw(self, surface):
        for direction, pressed in self.pressed.items():
            if pressed:
                arrow, (x, y) = self.pressed_placeholders[direction]
                arrow.draw(surface, x, y)

        if self.display_lives:
            font = ASSETS.font.PrimaSansBold[20]
            lives = font.render(
                str(self.player.lives), True, (0, 0, 0))
            lives_rect = lives.get_rect()
            lives_rect.center = (self.x + 162 + 44 // 2 + 1, 489 + 44 // 2 - 7)
            surface.blit(lives, lives_rect)

        font = ASSETS.font.PrimaSansBold[15]
        surface.blit(font.render(
            f"Score:   {self.player.score}", True, (0, 0, 0)), (self.x + 30, 487))
        surface.blit(font.render(
            f"Combo: {self.player.combo}", True, (0, 0, 0)), (self.x + 30, 506))

        for i, arrow in enumerate(self.player.arrows):
            arrow.draw(surface, self.xleft, i * 48)

        if self.player.doomed_by_satan > pygame.time.get_ticks():
            if self.doomed_cache[0] == self.player.doomed_by_satan:
                surface.blit(self.doomed_cache[1], (self.x + 18, 0))
            else:
                s = surface.subsurface((self.x + 18, 0, 202, 576)).copy()
                img = pygame.surfarray.pixels3d(s)
                img[:] = np.stack(
                    (np.dot(img, [0.2989, 0.5870, 0.1140]),)*3, axis=-1)
                del img
                self.doomed_cache = (self.player.doomed_by_satan, s)
        elif self.player.gifted_by_god > pygame.time.get_ticks():
            img = pygame.surfarray.pixels3d(
                surface.subsurface((self.x + 18, 0, 202, 576)))
            img[:] = np.clip(img * 1.7, 0, 255).astype(np.uint8)
            del img
        elif self.flash_time > pygame.time.get_ticks():
            surface.blit(ASSETS.image.flash, (self.x - 25, 0))
