from enum import Enum


class MessagePrioritiesEnum(Enum):
    CTRL = 0


class BaseMessage(object):
    priority = 0

    def __cmp__(self, other):
        return self.priority < other.priority


class CtrlMessage(BaseMessage):
    def __init__(self):
        self.priority = MessagePrioritiesEnum.CTRL.value
