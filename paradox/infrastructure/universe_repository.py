import json
from pathlib import Path

from pydantic import Field

from paradox.domain import Camera, Tile, Universe, UniverseRepository, ValueObject


class UniverseFile(ValueObject):
    name: str
    camera: Camera
    tiles: list[Tile]


class UniverseInfo(ValueObject):
    name: str = Field(default="New world")
    path: Path


class FileUniverseRepository(UniverseRepository):
    universes: dict[str, Universe] = {}
    universes_path: Path

    def __init__(self, universes_path: Path) -> None:
        self.universes_path = universes_path
        self.load_universes()

    def from_info(self, universe_info: UniverseInfo) -> Universe:
        json_path = self.universes_path.joinpath(universe_info.path)
        with json_path.open(mode="rt", encoding="utf-8") as stream:
            universe_file = UniverseFile.parse_obj(json.load(stream))
        
        mapping = {}
        for tile in universe_file.tiles:
            mapping[tile.coo] = tile

        return Universe(
            name=universe_file.name, camera=universe_file.camera, mapping=mapping
        )

    def load_universes(self) -> None:
        json_path = self.universes_path.joinpath("universes.json")
        with json_path.open(mode="rt", encoding="utf-8") as stream:
            universe_info_dicts = json.load(stream)

        for universe_info_dict in universe_info_dicts:
            universe_info = UniverseInfo.parse_obj(universe_info_dict)
            self.universes[universe_info.name] = self.from_info(universe_info)

    def get(self, name: str) -> Universe | None:
        return self.universes.get(name, None)
