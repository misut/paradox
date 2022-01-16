from paradox.engine import Engine
from paradox.settings import Settings


def load_settings() -> Settings:
    return Settings()


if __name__ == "__main__":
    settings = load_settings()
    
    engine = Engine(settings=settings)
