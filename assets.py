from __future__ import annotations
from typing import Dict, Tuple
from pathlib import Path
from abc import ABC

import pygame


class AssetManager:
    """
    An asset manager. You can get an asset like this: `manager.<asset type>.<asset name>`, if the asset name
    contains invalid characters you can do `manager.<asset type>["asset name"]`.
    """

    # The path of the asset folder.
    path: Path
    # Every asset type, with its name.
    AssetTypes: Dict[str, type]

    def __init__(self, path: Path):
        self.path = Path(path)
        self.AssetTypes = {name: AssetTypeProxy(
            self.path / prefix, AssetType) for name, (prefix, AssetType) in Asset.types.items()}

    def __getattr__(self, name: str) -> AssetTypeProxy:
        if name in self.AssetTypes:
            return self.AssetTypes[name]
        else:
            raise AttributeError(f"Unknown asset type: {name}")


class AssetTypeProxy:
    path: Path
    AssetType: type
    _cache = {}

    def __init__(self, path: Path, AssetType: Asset):
        self.path = path
        self.AssetType = AssetType
        self._cache = {}

    def __getattr__(self, name: str) -> Asset:
        if name in self._cache:
            return self._cache[name]
        else:
            for file in self.path.iterdir():
                if file.is_file() and file.stem == name:
                    asset = self.AssetType(name, file)
                    self._cache[name] = asset
                    return asset

    def __getitem__(self, name: str) -> Asset:
        return self.__getattr__(name)


class Asset(ABC):
    """The base class for every assets."""

    # Every type of asset, with its name and prefix.
    types: Dict[str, Tuple[Path, type]] = {}

    def __init_subclass__(cls, type: str, prefix: Path = "."):
        cls.types[type] = (Path(prefix), cls)

    # The name of this asset.
    name: str
    # The path of this asset.
    path: Path

    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path


class Image(Asset, type="image", prefix="images"):
    def __new__(cls, name: str, path: Path):
        return pygame.image.load(path).convert_alpha()


class Font(Asset, type="font", prefix="fonts"):
    """A font, cannot be used directly, you must do `font[font_size]` to actually get a font."""

    # The font cache
    _cache: Dict[int, pygame.font.Font]

    def __init__(self, name: str, path: Path):
        super().__init__(name, path)
        self._cache = {}

    def __getitem__(self, size: int) -> pygame.font.Font:
        if size not in self._cache:
            self._cache[size] = pygame.font.Font(self.path, size)
        return self._cache[size]


class Template(Asset, type="template", prefix="templates"):
    _cache: dict

    def __init__(self, name: str, path: Path):
        super().__init__(name, path)

        self._cache = {}

    def get(self, **kwargs) -> str:
        values = tuple(kwargs.values())
        if values not in self._cache:
            with open(self.path, "r") as f:
                result: str = f.read()

            while (pos := result.find("${")) != -1:
                end_pos = self._find_end_pos(result, pos + 2)
                expr = result[pos+2:end_pos-1].format(**kwargs)
                expr = eval(expr)
                result = result[:pos] + str(expr) + result[end_pos:]

            self._cache[values] = result
        return self._cache[values]

    def _find_end_pos(self, string: str, pos: int) -> int:
        """Find the closing `}` while accepting nested '{}'"""
        brackets = 1
        while brackets != 0:
            if string[pos] == "{":
                brackets += 1
            elif string[pos] == "}":
                brackets -= 1

            pos += 1

        return pos


Assets = AssetManager(Path(__file__).resolve().parent / "assets")
