from pydantic import BaseSettings


class Settings(BaseSettings):
    RENDER_SIZE: tuple[int, int]
    SCREEN_SIZE: tuple[int, int]

    class Config:
        env_file = ".env"
