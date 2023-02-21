import getpass
from pathlib import Path
from typing import Literal


class SaveManager:
    path: Path

    def __init__(self, path: Path):
        path.mkdir(exist_ok=True)
        self.path = path

        self.time_path = self.path / "time.txt"
        self.score_path = self.path / "score.txt"
        self.lives_path = self.path / "lives.txt"

    @property
    def time(self) -> (str, str):
        if self.time_path.exists():
            with open(self.time_path, 'r') as f:
                username, score = f.readlines()[-1].split("\t")
                return username, int(score)
        else:
            return None

    @property
    def score(self) -> (str, str):
        if self.score_path.exists():
            with open(self.score_path, 'r') as f:
                username, score = f.readlines()[-1].split("\t")
                return username, int(score)
        else:
            return None

    @property
    def lives(self) -> (str, str):
        if self.lives_path.exists():
            with open(self.lives_path, 'r') as f:
                username, score = f.readlines()[-1].split("\t")
                return username, int(score)
        else:
            return None

    def add(self, mode: Literal['lives', 'score', 'time'], score: int):
        if mode == 'time':
            highscore = self.time
            if highscore is None or score <= highscore:
                with open(self.time_path, 'a') as f:
                    f.write(f"{getpass.getuser()}\t{score}\n")
        elif mode == 'score':
            highscore = self.score
            if highscore is None or score >= highscore:
                with open(self.score_path, 'a') as f:
                    f.write(f"{getpass.getuser()}\t{score}\n")
        else:
            highscore = self.lives
            if highscore is None or score >= highscore:
                with open(self.lives_path, 'a') as f:
                    f.write(f"{getpass.getuser()}\t{score}\n")


SAVES = SaveManager(Path(__file__).resolve().parent / "saves")
