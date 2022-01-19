class ParadoxError(Exception):
    ...


class UIError(ParadoxError):
    ...


class UIAllocateError(UIError):
    ...
