from postoffice import Postman

from paradox.interface.protocols.action import action_postman
from paradox.interface.protocols.base import base_postman
from paradox.interface.protocols.event import event_postman
from paradox.interface.protocols.scene import scene_postman

chief_postman = Postman()
chief_postman.invite(
    action_postman,
    base_postman,
    event_postman,
    scene_postman,
)
