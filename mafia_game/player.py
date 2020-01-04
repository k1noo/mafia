from .roles import VillagerRole, MafiaRole, HealerRole, DetectiveRole, RoleEnum

from enum import Enum, unique, auto
from collections import defaultdict


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
        if role is not None:
            self.set_role(role)

    def set_role(self, role: RoleEnum):
        if role is RoleEnum.VILLAGER:
            self.role = VillagerRole()
        elif role is RoleEnum.MAFIA:
            self.role = MafiaRole()
        elif role is RoleEnum.HEALER:
            self.role = HealerRole()
        elif role is RoleEnum.DETECTIVE:
            self.role = DetectiveRole()
        else:
            raise ValueError("Unknown role to set {role_enum}".format(role_enum=role.name))

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

