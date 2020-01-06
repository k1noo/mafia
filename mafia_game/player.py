from .roles import RoleEnum, RoleFactory

from collections import defaultdict
from enum import Enum, unique, auto


@unique
class PlayerMode(Enum):
    ASLEEP = auto()
    AWAKENED = auto()


@unique
class PlayerStatus(Enum):
    ALIVE = auto()
    DEAD = auto()


class BasePlayer:
    def __init__(self, player_id: str, role: RoleEnum = None):
        self.__id = player_id
        self.__mode = PlayerMode.AWAKENED
        self.__killing_candidate = None

        self.role = None
        self.__role_factory = RoleFactory()
        if role is not None:
            self.set_role(role)

    def set_role(self, role: RoleEnum):
        self.role = self.__role_factory.generate_role(role)

    def set_killing_candidate(self, player: __class__):
        self.__killing_candidate = player

    def sleep(self):
        self.__mode = PlayerMode.ASLEEP

    def wakeup(self):
        self.__mode = PlayerMode.AWAKENED

    def day_vote(self, player: __class__):
        raise NotImplementedError

    def night_action(self, args: defaultdict):
        raise NotImplementedError


class OfflinePlayer(BasePlayer):
    def __init__(self, player_id, role):
        super().__init__(player_id, role)

    def day_vote(self, player):
        super().set_killing_candidate(player)

    def night_action(self, args: defaultdict):
        super().role.action()

