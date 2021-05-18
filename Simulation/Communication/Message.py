# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from enum import Enum


class MessageType(Enum):
    TASK_MOVE = ()
    TASK_SHOOT = ()
    ISR_CONTACT = ()


class Message:
    def __init__(self, _type, content):
        self._type = _type
        self.content = content
        self.sender = None
        self.receiver = None
        self.network = None

class MoveMessage(Message):
    def __init__(self, location):
        """

        :param location:
        """
        _type = MessageType.TASK_MOVE
        super().__init__(_type, location)


class ShootMessage(Message):
    def __init__(self, target, weapon):
        """

        :param target:
        :param weapon:
        """
        _type = MessageType.TASK_SHOOT
        content = [target, weapon]
        super().__init__(_type, content)


class DetectionMessage(Message):
    def __init__(self, contact):
        """

        :param contact:
        """
        _type = MessageType.ISR_CONTACT
        super().__init__(_type, contact)
