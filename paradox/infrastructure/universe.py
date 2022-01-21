from pathlib import Path

from pydantic import Field

from paradox.domain import Tile, Universe, UniverseRepository


class InMemoryUniverse(Universe):
    mapping: dict[tuple[int, int, int], Tile] = Field(default={})

    def at(self, coo: tuple[float, float, float]) -> Tile:
        _coo = tuple(map(int, coo))
        return self.mapping.get(_coo, Tile(coo=_coo))


class FileUniverseRepository(UniverseRepository):
    universes: dict[str, InMemoryUniverse] = {}
    universes_path: Path

    def __init__(self, universes_path: Path) -> None:
        self.universes_path = universes_path
    
    def get(self, name: str) -> Universe | None:
        return self.universes.get(name, None)
