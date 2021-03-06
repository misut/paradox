from pydantic import Field

from paradox.domain.apparition.base import Apparition


class Character(Apparition):
    jump_count: int = Field(default=0)
    jump_limit: int = Field(default=0)
    jump_velocity: float = Field(default=20.0)

    @property
    def jumping(self) -> bool:
        return self.fall_velocity < 0.0

    def can_jump(self) -> None:
        if self.jump_count >= self.jump_limit:
            return False
        return True

    def jump(self) -> None:
        if not self.can_jump():
            return None

        self.jump_count += 1
        self.fall_velocity = -self.jump_velocity

    def load(self) -> None:
        super().load()

        self.jump_count = 0
