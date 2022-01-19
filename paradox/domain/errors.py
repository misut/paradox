class ParadoxError(Exception):
    ...


class SpriteLoadError(ParadoxError):
    ...


class UIError(ParadoxError):
    ...


class UIAllocateError(UIError):
    ...
