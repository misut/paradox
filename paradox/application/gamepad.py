from loguru import logger
from pydantic import BaseModel, Field

from paradox.domain.actions import (
    Action,
    ActionType,
    LeftAction,
    RightAction,
    UpAction,
    DownAction,
)
import pygame


class Gamepad(BaseModel):
    mapping: dict[int, type[Action]] = Field(default={})
    scanning: dict[type[Action], int] = Field(default={})

    def __init__(self) -> None:
        super().__init__()

        self.mapping[4] = LeftAction
        self.mapping[7] = RightAction
        self.mapping[26] = UpAction
        self.mapping[22] = DownAction

        actions = [LeftAction, RightAction, UpAction, DownAction]
        for action in actions:
            self.scanning[action] = 0

    def poll(self, ticks: int) -> list[Action]:
        actions = []

        scancodes = pygame.key.get_pressed()
        for key, pressed in enumerate(scancodes):
            action = self.mapping.get(key, None)
            if action == None:
                continue
            
            if pressed:
                if self.scanning[action] > 0:
                    action_type = ActionType.PRESSING
                else:
                    action_type = ActionType.PRESSED
                self.scanning[action] += ticks
                actions.append(action(type=action_type, duration=self.scanning[action]))
                logger.info(f"{action.__name__} is {action_type.name} during {self.scanning[action]} msec.")
            elif self.scanning[action] > 0:
                action_type = ActionType.RELEASED
                actions.append(action(type=action_type, duration=self.scanning[action]))
                logger.info(f"{action.__name__} is {action_type.name} during {self.scanning[action]} msec.")
                self.scanning[action] = 0
            
        return actions
