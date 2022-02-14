from collections.abc import Callable

from pydantic import Field

from paradox.domain.action import Action, ActionInfo, ActionInfoTable
from paradox.domain.base import Entity, Updatable

Stunt = Callable[[ActionInfo], None]


class Stuntman(Entity, Updatable):
    stunts: dict[Action, Stunt] = Field(default=None)

    def learn(self, action: Action) -> Callable[[Stunt], Stunt]:
        def decorator(stunt: Stunt) -> Stunt:
            self.stunts[action] = stunt
            return stunt
        
        return decorator

    def stunt(self, action_infos: ActionInfoTable) -> None:
        for action, action_info in action_infos.items():
            self.stunts[action](action_info)

    def update(self, ticks: int) -> None:
        super().update(ticks)

        
