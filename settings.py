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


SETTINGS = Settings()
