from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    RENDER_SIZE: tuple[int, int]
    SCREEN_SIZE: tuple[int, int]
    TILE_SIZE: tuple[int, int]
    WALL_SIZE: tuple[int, int]

    ASSETS_PATH: Path
    SPRITES_PATH: Path

    class Config:
        env_file = ".env"
        env_prefix = "PARADOX_"
