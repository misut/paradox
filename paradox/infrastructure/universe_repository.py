import json
from pathlib import Path

from pydantic import Field

from paradox.domain import (
    Camera,
    SpriteTag,
    Tile,
    Universe,
    UniverseRepository,
    ValueObject,
)


class UniverseFile(ValueObject):
    name: str = Field(default="New world")
    camera: Camera
    tiles: list[Tile]


class FileUniverseRepository(UniverseRepository):
    universes: dict[str, Universe] = {}
    universes_path: Path

    def __init__(self, universes_path: Path) -> None:
        self.universes_path = universes_path

        self.load_universes()

    def from_file(self, universe_file: UniverseFile) -> Universe:
        mapping = {}
        for tile in universe_file.tiles:
            mapping[tile.coo] = tile

        return Universe(
            name=universe_file.name, camera=universe_file.camera, mapping=mapping
        )

    def load_universes(self) -> None:
        json_path = self.universes_path.joinpath("universes.json")
        with json_path.open(mode="rt", encoding="utf-8") as stream:
            universe_file_dicts = json.load(stream)

        for universe_file_dict in universe_file_dicts:
            universe_file = UniverseFile.parse_obj(universe_file_dict)
            self.universes[universe_file.name] = self.from_file(universe_file)

    def get(self, name: str) -> Universe | None:
        return self.universes.get(name, None)
