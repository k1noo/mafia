from .roles import RoleEnum, RoleFactory, TeamEnum

from enum import Enum, unique, auto
from collections import defaultdict


@unique
class GamePhase(Enum):
    DAY = auto()
    NIGHT = auto()


class MafiaGame:
    def __init__(self, mafia_coefficient: int = 4, banned_roles: list = None):
        self.__players = defaultdict()
        self.__mafia_count = 0
        self.__phase = GamePhase.DAY
        self.__mafia_coefficient = max(mafia_coefficient, 1)
        self.__roles_factory = RoleFactory()

        self.__available_roles = defaultdict(bool, ((role, True) for role in RoleEnum))
        if banned_roles is not None:
            for role in banned_roles:
                self.__available_roles[role] = False

    def __calculate_max_mafia_count(self):
        return len(self.__players) // self.__mafia_coefficient

    @staticmethod
    def __get_roles_by_team(roles: list, team: TeamEnum):
        return [role for role in roles if role.get_team() is team]

    def __get_packed_roles(self, roles, count_to_pack):
        result = []
        roles_to_pack = roles.copy()
        while count_to_pack > 0 and len(roles_to_pack) > 0:
            if not self.__available_roles.get(roles_to_pack[-1].get_name()):
                roles_to_pack.pop()
            else:
                role = self.__roles_factory.generate_role(roles_to_pack[-1].get_name())
                if role.is_unique():
                    self.__available_roles[role.get_name()] = False
                result.append(role)
                count_to_pack -= 1
        return result

    def __generate_roles(self):
        result = []
        roles = [self.__roles_factory.generate_role(role_enum)
                 for role_enum in self.__available_roles.keys()
                 if self.__available_roles.get(role_enum)]

        mafia_team_roles = self.__get_roles_by_team(roles, TeamEnum.MAFIA)
        mafias = self.__get_packed_roles(mafia_team_roles, self.__mafia_count)

    def __assign_roles(self):
        pass
