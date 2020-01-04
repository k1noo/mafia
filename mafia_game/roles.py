from enum import Enum, unique, auto


@unique
class TeamEnum(Enum):
    MAFIA = auto()
    CIVILIAN = auto()


@unique
class RoleEnum(Enum):
    VILLAGER = auto()
    MAFIA = auto()
    HEALER = auto()
    DETECTIVE = auto()


class RoleWeight(Enum):
    VILLAGER = 0
    MAFIA = 0
    HEALER = 1
    DETECTIVE = 1


class RolePriority(Enum):
    VILLAGER = 0
    MAFIA = 0
    HEALER = 1
    DETECTIVE = 2


class BaseRole(object):
    def get_name(self):
        raise NotImplementedError

    def get_team(self):
        raise NotImplementedError

    def get_priority(self):
        raise NotImplementedError

    def get_weight(self):
        raise NotImplementedError

    def action(self):
        pass


class VillagerRole(BaseRole):
    def get_name(self):
        return "villager"

    def get_team(self):
        return TeamEnum.CIVILIAN

    def get_priority(self):
        return RolePriority.VILLAGER.value

    def get_weight(self):
        return RoleWeight.VILLAGER.value


class MafiaRole(BaseRole):
    def get_name(self):
        return "mafia"

    def get_team(self):
        return TeamEnum.MAFIA

    def get_priority(self):
        return RolePriority.MAFIA.value

    def get_weight(self):
        return RoleWeight.MAFIA.value


class HealerRole(BaseRole):
    def get_name(self):
        return "healer"

    def get_team(self):
        return TeamEnum.CIVILIAN

    def get_priority(self):
        return RolePriority.HEALER.value

    def get_weight(self):
        return RoleWeight.HEALER.value


class DetectiveRole(BaseRole):
    def get_name(self):
        return "detective"

    def get_team(self):
        return TeamEnum.CIVILIAN

    def get_priority(self):
        return RolePriority.DETECTIVE.value

    def get_weight(self):
        return RoleWeight.DETECTIVE.value
