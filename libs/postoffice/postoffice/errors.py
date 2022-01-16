class PostofficeError(Exception):
    ...


class PostNotSubscribedError(PostofficeError):
    ...


class PostbusNotEmpty(PostofficeError):
    ...
