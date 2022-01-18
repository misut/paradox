from typing import Generator

from pydantic import BaseModel
from pytest import fixture, raises

from atelier import PaletteNotOccupiedError, Portrayer


class NotOccupiedPalette(BaseModel):
    ...


class ThisPalette(BaseModel):
    ...


class ThatPalette(BaseModel):
    ...


@fixture(name="not_occupied_palette", scope="module")
def create_not_occupied_palette() -> Generator[NotOccupiedPalette, None, None]:
    yield NotOccupiedPalette()


def test_apprentice_portrayer(not_occupied_palette: NotOccupiedPalette) -> None:
    portrayer = Portrayer()

    with raises(PaletteNotOccupiedError):
        portrayer.portray(not_occupied_palette)


def test_occupy_and_portray() -> None:
    veteran_portrayer = Portrayer()

    @veteran_portrayer.occupy()
    def this_method(palette: ThisPalette) -> None:
        pass

    apprentice_portrayer = Portrayer()

    @apprentice_portrayer.occupy()
    def this_method(palette: ThatPalette) -> None:
        pass

    veteran_portrayer.invite(apprentice_portrayer)

    veteran_portrayer.portray(ThisPalette())
    veteran_portrayer.portray(ThatPalette())
