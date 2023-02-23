import pygame

from game import Player
from arrow import Arrow, Direction
from assets import ASSETS
from settings import SETTINGS
from widgets.lane import PlayerLane

from . import Scene
from .gameover_2p import GameOver2p


class Game2p(Scene):
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.lane1 = PlayerLane(25, self.player1)
        self.lane2 = PlayerLane(313, self.player2)

        background = ASSETS.image.background.copy()
        background.blit(ASSETS.image.game_base, (0, 0))
        self.lane1.draw_background(background)
        self.lane2.draw_background(background)
        if SETTINGS.time is not None:
            timer_rect = ASSETS.image.timer.get_rect()
            timer_rect.centerx = 576 // 2
            timer_rect.y = 204
            self.timer_rect = timer_rect
            background.blit(ASSETS.image.timer, timer_rect)
            self.start_time = pygame.time.get_ticks()

        super().__init__(background)

        if SETTINGS.lives is not None:
            self.player1.lives = SETTINGS.lives
            self.player2.lives = SETTINGS.lives
        self.player1.arrows = [Arrow.get() for _ in range(10)]
        self.player2.arrows = [Arrow.get() for _ in range(10)]
        self.key_lookup = {
            SETTINGS.p1_controls.left: (self.lane1, Direction.Left),
            SETTINGS.p1_controls.up: (self.lane1, Direction.Up),
            SETTINGS.p1_controls.down: (self.lane1, Direction.Down),
            SETTINGS.p1_controls.right: (self.lane1, Direction.Right),
            SETTINGS.p2_controls.left: (self.lane2, Direction.Left),
            SETTINGS.p2_controls.up: (self.lane2, Direction.Up),
            SETTINGS.p2_controls.down: (self.lane2, Direction.Down),
            SETTINGS.p2_controls.right: (self.lane2, Direction.Right),
        }

    def tick(self, _):
        if SETTINGS.time is not None and pygame.time.get_ticks() - self.start_time > (SETTINGS.time * 1000):
            self.gameover()

    def draw(self, surface):
        super().draw(surface)

        if SETTINGS.time is not None:
            time_font = ASSETS.font.PrimaSansBold[30]
            time = SETTINGS.time - \
                (pygame.time.get_ticks() - self.start_time) // 1000
            time = time_font.render(str(time), True, (0, 0, 0))
            time_rect = time.get_rect()
            time_rect.centerx = self.timer_rect.centerx + 1
            time_rect.centery = self.timer_rect.centery - 2
            surface.blit(time, time_rect)

        self.lane1.draw(surface)
        self.lane2.draw(surface)

    def key_pressed(self, lane, direction):
        lane.key_pressed(direction)

        if SETTINGS.score is not None and lane.player.score >= SETTINGS.score:
            self.gameover()
        if SETTINGS.lives is not None and lane.player.lives <= 0:
            self.gameover()

    def gameover(self):
        if self.player1.score == self.player2.score:
            winner = 'tie'
        else:
            winner = 'player1' if self.player1.score > self.player2.score else 'player2'
        self.manager.goto(GameOver2p(
            winner, self.player1.score, self.player2.score), reset=True)

    def back(self):
        self.gameover()

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key in self.key_lookup:
            lane, direction = self.key_lookup[event.key]
            lane.pressed[direction] = True
            self.key_pressed(lane, direction)
            return False
        elif event.type == pygame.KEYUP and event.key in self.key_lookup:
            lane, direction = self.key_lookup[event.key]
            lane.pressed[direction] = False

        return super().event(event)
