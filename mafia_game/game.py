from .messaging import CtrlMessage, GamePlayMessage, PlayerCtrlMessage, GameSessionCtrlMessage
from .player import OfflinePlayer
from .roles import RoleEnum, RoleFactory, TeamEnum

from collections import defaultdict
from enum import auto, Enum, unique
from queue import PriorityQueue, Empty
from random import choices, shuffle
from string import ascii_uppercase, digits

import logging

GAME_TOKEN_LENGTH = 4
QUEUE_TIMEOUT = 1


@unique
class GamePhase(Enum):
    DAY = auto()
    NIGHT = auto()


class DayPhaseStage(Enum):
    VOTING = auto()
    HANGING = auto()
    LAST_WORD = auto()


class NightPhaseStage(Enum):
    CIVILIANS = auto()
    MAFIA = auto()


class MafiaGame:
    def __init__(self, mafia_coefficient: int = 4, banned_roles: list = None, logger=None, loglevel=logging.DEBUG):
        self.token = ''.join(choices(ascii_uppercase + digits, k=GAME_TOKEN_LENGTH))
        self.inbox_messages_queue = PriorityQueue()
        self.is_running = False

        self.__players = defaultdict()
        self.__mafia_count = 0
        self.__phase = GamePhase.DAY
        self.__mafia_coefficient = max(mafia_coefficient, 1)
        self.__role_factory = RoleFactory()

        self.__available_roles = defaultdict(bool, ((role, True) for role in RoleEnum))
        if banned_roles is not None:
            for role in banned_roles:
                self.__available_roles[role] = False

        self.__logger = logger
        if self.__logger is None:
            self.__logger = logging.getLogger("MafiaGame_{token}".format(token=self.token))
            self.__logger.setLevel(loglevel)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            self.__logger.addHandler(ch)

        self.__logger.info("Created game session `{token}`. Mafias count = N // k, where k is {k}."
                           " Available roles: {roles}"
                           .format(token=self.token,
                                   k=self.__mafia_coefficient,
                                   roles=", ".join([k for k, v in self.__available_roles.items() if v])))

    def __calculate_max_mafia_count(self):
        return len(self.__players) // self.__mafia_coefficient

    @staticmethod
    def __get_roles_by_team(roles: list, team: TeamEnum):
        return [role for role in roles if role.get_team() is team]

    def __get_packed_roles(self, roles, count_to_pack):
        result = []
        roles_to_pack = sorted(roles, key=lambda x: x.get_priority())
        while count_to_pack > 0 and len(roles_to_pack) > 0:
            if not self.__available_roles.get(roles_to_pack[-1].get_name()):
                roles_to_pack.pop()
            else:
                role = self.__role_factory.generate_role(roles_to_pack[-1].get_name())
                if role.is_unique():
                    self.__available_roles[role.get_name()] = False
                result.append(role)
                count_to_pack -= 1
        return result

    def __generate_roles(self):
        roles = [self.__role_factory.generate_role(role_enum)
                 for role_enum in self.__available_roles.keys()
                 if self.__available_roles.get(role_enum)]

        mafia_team_roles = self.__get_roles_by_team(roles, TeamEnum.MAFIA)
        mafias = self.__get_packed_roles(mafia_team_roles, self.__mafia_count)
        self.__logger.debug("Mafia roles to assign: {mafias}".format(
            mafias=", ".join([role.get_name().name for role in mafias])))

        civilians_team_roles = self.__get_roles_by_team(roles, TeamEnum.CIVILIAN)
        civilians_count = max(len(self.__players) - self.__mafia_count, 0)
        civilians = self.__get_packed_roles(civilians_team_roles, civilians_count)
        self.__logger.debug("Civilians roles to assign: {civilians}".format(
            civilians=", ".join([role.get_name().name for role in civilians])))

        result = mafias + civilians
        shuffle(result)
        self.__logger.debug("Shuffled roles to assign: {shuffled}".format(
            shuffled=", ".join([role.get_name().name for role in result])))
        return result

    def __assign_roles(self):
        roles = self.__generate_roles()
        for player in self.__players.values():
            if len(roles) > 0:
                player.set_role(roles.pop().get_name())

    def __switch_phase(self):
        current_role = self.__phase
        if self.__phase is GamePhase.DAY:
            self.__phase = GamePhase.NIGHT
        else:
            self.__phase = GamePhase.DAY
        self.__logger.info("Game phase switched {prev}->{curr}".format(prev=current_role.name, curr=self.__phase.name))

    def __register_player(self, player_id):
        if not self.__players.get(player_id, False):
            self.__players[player_id] = OfflinePlayer(player_id)
            self.__logger.info("Player {player_id} has been registered in game {token}".format(
                player_id=player_id, token=self.token))
        else:
            self.__logger.info("Player {player_id} is already registered in game {token}".format(
                player_id=player_id, token=self.token))

    def __remove_player(self, player_id):
        if not self.__players.get(player_id, False):
            self.__logger.info("Player {player_id} does not exist in game {token}".format(
                player_id=player_id, token=self.token))
        else:
            self.__players.pop(player_id)
            self.__logger.info("Player {player_id} has left the game {token}".format(
                player_id=player_id, token=self.token))

    def __process_ctrl_message(self, message: CtrlMessage):
        if isinstance(message, PlayerCtrlMessage):
            if message.type is PlayerCtrlMessage.Type.REGISTER:
                self.__register_player(message.player_id)
            elif message.type is PlayerCtrlMessage.Type.LEAVE:
                self.__remove_player(message.player_id)
            else:
                self.__logger.info("Unknown PlayerCtrlMessage type received: {t}".format(t=message.type.name))
        elif isinstance(message, GameSessionCtrlMessage):
            pass
        pass

    def __process_game_play_message(self, message: GamePlayMessage):
        pass

    def __game_loop(self):
        while self.is_running:
            try:
                message = self.inbox_messages_queue.get(timeout=1)
                if issubclass(message, CtrlMessage):
                    self.__process_ctrl_message(message)
                elif issubclass(message, GamePlayMessage):
                    self.__process_game_play_message(message)
            except Empty:
                continue
        pass

    def run(self):
        pass
