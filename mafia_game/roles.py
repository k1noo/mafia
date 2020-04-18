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

    def is_unique(self):
        raise NotImplementedError

    def action(self):
        pass

    def __str__(self):
        return self.get_name().name


class VillagerRole(BaseRole):
    def get_name(self):
        return RoleEnum.VILLAGER

    def get_team(self):
        return TeamEnum.CIVILIAN

    def get_priority(self):
        return RolePriority.VILLAGER.value

    def get_weight(self):
        return RoleWeight.VILLAGER.value

    def is_unique(self):
        return False


class MafiaRole(BaseRole):
    def get_name(self):
        return RoleEnum.MAFIA

    def get_team(self):
        return TeamEnum.MAFIA

    def get_priority(self):
        return RolePriority.MAFIA.value

    def get_weight(self):
        return RoleWeight.MAFIA.value

    def is_unique(self):
        return False


class HealerRole(BaseRole):
    def get_name(self):
        return RoleEnum.HEALER

    def get_team(self):
        return TeamEnum.CIVILIAN

    def get_priority(self):
        return RolePriority.HEALER.value

    def get_weight(self):
        return RoleWeight.HEALER.value

    def is_unique(self):
        return True


class DetectiveRole(BaseRole):
    def get_name(self):
        return RoleEnum.DETECTIVE

    def get_team(self):
        return TeamEnum.CIVILIAN

    def get_priority(self):
        return RolePriority.DETECTIVE.value

    def get_weight(self):
        return RoleWeight.DETECTIVE.value

    def is_unique(self):
        return True


class RoleFactory(object):
    @staticmethod
    def generate_role(role: RoleEnum):
        if role is RoleEnum.VILLAGER:
            return VillagerRole()
        elif role is RoleEnum.MAFIA:
            return MafiaRole()
        elif role is RoleEnum.HEALER:
            return HealerRole()
        elif role is RoleEnum.DETECTIVE:
            return DetectiveRole()
        else:
            raise ValueError("Unknown role to generate: {role_enum}".format(role_enum=role.name))
