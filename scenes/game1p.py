import pygame

from game import Mode, Player
from arrow import Arrow, Direction
from saves import SAVES
from assets import ASSETS
from settings import SETTINGS
from widgets.lane import PlayerLane

from . import Scene
from .gameover_1p import GameOver1p


class Game1p(Scene):
    def __init__(self, mode: Mode):
        self.player = Player()
        self.lane = PlayerLane(
            169, self.player, display_lives=mode is Mode.Lives or (mode is Mode.Custom and SETTINGS.lives is not None))

        background = ASSETS.image.background.copy()
        background.blit(ASSETS.image.game_base, (0, 0))
        self.lane.draw_background(background)

        self._start_time = None
        self.greyed_cache = None

        self.end_time = None
        if mode is Mode.Time \
           or mode is Mode.Score \
           or (mode is Mode.Custom and SETTINGS.time is not None):
            timer_rect = ASSETS.image.timer.get_rect()
            timer_rect.x = 96
            timer_rect.y = 397
            self.timer_rect = timer_rect
            background.blit(ASSETS.image.timer, timer_rect)

        super().__init__(background)
        self.mode = mode

        self.end_time = None
        if mode is Mode.Time:
            self.end_time = 30
        elif mode is Mode.Custom:
            self.end_time = SETTINGS.time

        self.lives_enabled = False
        if mode is Mode.Lives or (mode is Mode.Custom and SETTINGS.lives is not None):
            self.lives_enabled = True
            self.player.lives = SETTINGS.lives if mode is Mode.Custom else 5

        self.max_score = None
        if mode in (Mode.Score, Mode.Custom):
            self.max_score = SETTINGS.score if mode is Mode.Custom else 2000

        self.player.arrows = [Arrow.get() for _ in range(10)]
        self.key_lookup = {
            SETTINGS.p1_controls.left: Direction.Left,
            SETTINGS.p1_controls.up: Direction.Up,
            SETTINGS.p1_controls.down: Direction.Down,
            SETTINGS.p1_controls.right: Direction.Right,
        }

        self.countdown = pygame.time.get_ticks() + 4000

    @property
    def start_time(self):
        return self._start_time or pygame.time.get_ticks()

    def tick(self, _):
        if self.countdown < pygame.time.get_ticks() and self._start_time is None:
            self._start_time = pygame.time.get_ticks()
            return

        if self.end_time is not None and pygame.time.get_ticks() - self.start_time > (self.end_time * 1000):
            self.gameover()

    def draw(self, surface):
        super().draw(surface)

        time = None
        if self.end_time is not None:
            time = self.end_time - \
                (pygame.time.get_ticks() - self.start_time) // 1000
        elif self.mode is Mode.Score:
            time = (pygame.time.get_ticks() - self.start_time) // 1000

        if time is not None:
            font = ASSETS.font.PrimaSansBold[30]
            time = font.render(str(time), True, (0, 0, 0))
            time_rect = time.get_rect()
            time_rect.centerx = self.timer_rect.centerx + 1
            time_rect.centery = self.timer_rect.centery - 2
            surface.blit(time, time_rect)

        self.lane.draw(surface)

        if self.greyed_cache is None:
            self.greyed_cache = surface.copy()
            img = pygame.surfarray.pixels3d(self.greyed_cache)
            img[:] = img // 2
            del img

        if self.countdown > pygame.time.get_ticks():
            surface.blit(self.greyed_cache, (0, 0))

            countdown = (self.countdown - pygame.time.get_ticks()) // 1000
            if countdown == 0:
                countdown = "GO"
            countdown = ASSETS.font.PrimaSansBold[50].render(
                str(countdown), True, (255, 0, 0))
            countdown_rect = countdown.get_rect()
            countdown_rect.center = (576//2, 576//2)
            surface.blit(countdown, countdown_rect)

    def key_pressed(self, direction):
        self.lane.key_pressed(direction)

        if self.max_score is not None and self.player.score >= self.max_score:
            self.gameover()
        if self.lives_enabled and self.player.lives <= 0:
            self.gameover()

    def gameover(self):
        score = self.player.score
        if self.mode == Mode.Score:
            score = (pygame.time.get_ticks() -
                     self.start_time) // 1000

        if self.mode != Mode.Custom:
            SAVES.add(self.mode, score)
        self.manager.goto(GameOver1p(self.mode, score))

    def event(self, event):
        if not self.countdown > pygame.time.get_ticks():
            if event.type == pygame.KEYDOWN and event.key in self.key_lookup:
                direction = self.key_lookup[event.key]
                self.lane.pressed[direction] = True
                self.key_pressed(direction)
                return False
            elif event.type == pygame.KEYUP and event.key in self.key_lookup:
                direction = self.key_lookup[event.key]
                self.lane.pressed[direction] = False

        return super().event(event)
