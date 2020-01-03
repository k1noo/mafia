from .roles import Villager, Mafia, Healer, Detective

from enum import Enum, unique, auto
from collections import defaultdict


@unique
class RoleEnum(Enum):
    VILLAGER = auto()
    MAFIA = auto()
    HEALER = auto()
    DETECTIVE = auto()


@unique
class PlayerMode(Enum):
    ASLEEP = auto()
    AWAKENED = auto()


class BasePlayer:
    def __init__(self, player_id: str, role: RoleEnum):
        self.__id = player_id
        self.__mode = PlayerMode.AWAKENED
        self.__killing_candidate = None

        self.role = None
        if role is RoleEnum.VILLAGER:
            self.__role = Villager()
        elif role is RoleEnum.MAFIA:
            self.__role = Mafia()
        elif role is RoleEnum.HEALER:
            self.__role = Healer()
        elif role is RoleEnum.DETECTIVE:
            self.__role = Detective()

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

