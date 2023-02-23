from typing import Optional
from dataclasses import dataclass

import pygame


@dataclass
class PlayerControls:
    left: int
    up: int
    down: int
    right: int


@dataclass
class Settings:
    p1_controls: PlayerControls = \
        PlayerControls(pygame.K_q, pygame.K_z, pygame.K_s, pygame.K_d)
    p2_controls: PlayerControls = \
        PlayerControls(pygame.K_KP4, pygame.K_KP8, pygame.K_KP5, pygame.K_KP6)

    # Used in custom solo and duel. If it's not None the game
    # will end after x seconds.
    time: Optional[int] = None
    # Used in custom solo and duel. If it's not None the game
    # will end when a player get to this score.
    score: Optional[int] = None
    # Used in custom solo and duel. If it's not None the players
    # will start with x lives, and the game will stop when
    # they get to 0.
    lives: Optional[int] = None


SETTINGS = Settings()
