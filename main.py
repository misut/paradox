import sys

from paradox.interface import BaseSettings, Engine, GamepadSettings, GraphicSettings

if __name__ == "__main__":
    engine = Engine(
        base_settings=BaseSettings(),
        gamepad_settings=GamepadSettings(),
        graphic_settings=GraphicSettings(),
    )
