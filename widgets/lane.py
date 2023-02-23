import pygame

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
        failed = self.player.arrows[-1].pressed(self.player, direction)
        if not failed:
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

        if self.flash_time > pygame.time.get_ticks():
            surface.blit(ASSETS.image.flash, (self.x - 25, 0))
