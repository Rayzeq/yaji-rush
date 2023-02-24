from __future__ import annotations
from typing import Dict, Tuple, Union, BinaryIO
from pathlib import Path
from abc import ABC
import io

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

    def _get_asset_path(self, name: str) -> Path:
        for file in self.path.iterdir():
            if file.is_file() and file.stem == name:
                return file
        raise ValueError(f"No asset named `{name}`")

    def _get_template_name(self, name: str, **kwargs):
        kwargs = sorted(list(kwargs.items()), key=lambda x: x[0])
        return name + '-' + '-'.join(str(x[1]) for x in kwargs)

    def _get_png_path(self, name: str, **kwargs) -> Path:
        return self._get_asset_path(self._get_template_name(name, **kwargs))

    def __getattr__(self, name: str) -> Asset:
        if name in self._cache:
            return self._cache[name]
        else:
            path = self._get_asset_path(name)
            asset = self.AssetType(name, path)
            self._cache[name] = asset
            return asset

    def __getitem__(self, name: str) -> Asset:
        return self.__getattr__(name)

    def template(self, name: str, **kwargs):
        cache_key = (name, *kwargs.values())

        if cache_key not in self._cache:
            try:
                path = self._get_asset_path(name)
            except ValueError:
                path = self._get_png_path(name, **kwargs)
                self._cache[cache_key] = self.AssetType(name, path)
            else:
                with open(path, "r") as f:
                    result: str = f.read()

                while (pos := result.find("${")) != -1:
                    end_pos = self._find_end_pos(result, pos + 2)
                    expr = result[pos+2:end_pos-1].format(**kwargs)
                    expr = eval(expr)
                    result = result[:pos] + str(expr) + result[end_pos:]

                self._cache[cache_key] = self.AssetType(
                    name, io.BytesIO(result.encode()))
                if self.AssetType is Image:
                    name = self._get_template_name(name, **kwargs)
                    pygame.image.save(
                        self._cache[cache_key], self.path / (name + '.png'))

        return self._cache[cache_key]

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


class Asset(ABC):
    """The base class for every assets."""

    # Every type of asset, with its name and prefix.
    types: Dict[str, Tuple[Path, type]] = {}

    def __init_subclass__(cls, type: str, prefix: Path = "."):
        cls.types[type] = (Path(prefix), cls)

    # The name of this asset.
    name: str
    # The path or file of this asset.
    path: Union[Path, BinaryIO]

    def __init__(self, name: str, path: Union[Path, BinaryIO]):
        self.name = name
        self.path = path


class Image(Asset, type="image", prefix="images"):
    def __new__(cls, name: str, path: Path):
        img = pygame.image.load(path).convert_alpha()
        if isinstance(path, Path) and path.suffix == ".svg":
            pygame.image.save(img, path.parent / (path.stem + ".png"))
        return img


class Font(Asset, type="font", prefix="fonts"):
    """A font asset, cannot be used directly, you must do `font[font_size]` to actually get a font."""

    # The font cache
    _cache: Dict[int, pygame.font.Font]

    def __init__(self, name: str, path: Union[Path, BinaryIO]):
        super().__init__(name, path)
        self._cache = {}

    def __getitem__(self, size: int) -> pygame.font.Font:
        if size not in self._cache:
            self._cache[size] = pygame.font.Font(self.path, size)
        return self._cache[size]


ASSETS = AssetManager(Path(__file__).resolve().parent / "assets")
