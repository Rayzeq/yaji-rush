from dataclasses import dataclass, field
from enum import Enum, auto


class Mode(Enum):
    Time = auto()
    Score = auto()
    Lives = auto()
    Custom = auto()


@dataclass
class Player:
    score: int = 0
    lives: int = 0
    combo: int = 0
    arrows: list = field(default_factory=list)
    doomed_by_satan: int = 0
    gifted_by_god: int = 0
