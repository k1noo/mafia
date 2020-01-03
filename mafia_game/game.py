from enum import Enum, unique, auto


@unique
class GamePhase(Enum):
    DAY = auto()
    NIGHT = auto()


class MafiaGame:
    def __init__(self):
        self.__players = []
        self.__mafia_count = 0

