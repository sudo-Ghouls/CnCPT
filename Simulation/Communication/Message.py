# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from copy import copy
from enum import Enum


class MessageType(Enum):
    TASK_MOVE = ()
    TASK_SHOOT = ()
    ISR_CONTACT = ()


class Message:
    def __init__(self, _type, content, time):
        self.type = _type
        self.content = content
        self.time = time
        self.sender = None
        self.receiver = None
        self.network = None


class MoveMessage(Message):
    def __init__(self, location, time):
        """

        :param location:
        """
        _type = MessageType.TASK_MOVE
        super().__init__(_type, location, time)


class ShootMessage(Message):
    def __init__(self, target, weapon, time):
        """

        :param target:
        :param weapon:
        """
        _type = MessageType.TASK_SHOOT
        content = [target, weapon]
        super().__init__(_type, content, time)


class DetectionMessage(Message):
    def __init__(self, contact, time):
        """

        :param contact:
        """
        content = {contact.target_name_truth: copy(contact)}
        _type = MessageType.ISR_CONTACT
        super().__init__(_type, content, time)
