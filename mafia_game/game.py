from .roles import RoleEnum

from enum import Enum, unique, auto
from collections import defaultdict


@unique
class GamePhase(Enum):
    DAY = auto()
    NIGHT = auto()


class MafiaGame:
    def __init__(self, mafia_coefficient=4, banned_roles: list = None):
        self.__players = defaultdict()
        self.__mafia_count = 0
        self.__phase = GamePhase.DAY
        self.__mafia_coefficient = max(mafia_coefficient, 1)

        self.__available_roles = defaultdict(bool, ((role, True) for role in RoleEnum))
        if banned_roles is not None:
            for role in banned_roles:
                self.__available_roles[role] = False

    def __calculate_max_mafia_count(self):
        return len(self.__players) // self.__mafia_coefficient

    def __assign_roles(self):

        pass
