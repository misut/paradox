from pathlib import Path

from pydantic import BaseSettings as PydanticBaseSettings


class BaseSettings(PydanticBaseSettings):
    ASSETS_PATH: Path
    FONTS_PATH: Path
    SPRITES_PATH: Path
    UNIVERSES_PATH: Path

    class Config:
        env_file = ".env"
        env_prefix = "PARADOX_"


class GamepadSettings(PydanticBaseSettings):
    LEFT: int
    RIGHT: int
    UP: int
    DOWN: int
    JUMP: int

    class Config:
        env_file = ".env"
        env_prefix = "PARADOX_GAMEPAD_"


class GraphicSettings(PydanticBaseSettings):
    RENDER_SIZE: tuple[int, int]
    SCREEN_SIZE: tuple[int, int]

    class Config:
        env_file = ".env"
        env_prefix = "PARADOX_GRAPHIC_"
