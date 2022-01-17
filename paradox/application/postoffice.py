from postoffice import Postoffice

from paradox.application.delivery_protocols import chief_postman


class ParadoxPostoffice(Postoffice):
    def __init__(self) -> None:
        super().__init__()

        self.hire(chief_postman)
